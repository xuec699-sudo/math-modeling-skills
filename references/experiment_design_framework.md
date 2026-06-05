# 实验设计框架 (Experiment Design Framework)

> **位置**: pipeline stage `experiment_design`，位于 `data_preprocessing` 之后、`model_N_build` 之前。
> **目的**: 在开始建模前，系统性地规划每个子问题的实验方案，避免盲目试算法。

---

## 实验设计模板

每个子问题 `model_N` 必须填写以下实验设计卡：

```yaml
model_id: model_1
problem_description: "子问题1的简要描述"
depends_on: []  # 依赖的其他模型 ID，如 ["model_2"] 表示需要 model_2 的结果

## 1. 模型选择论证
candidate_models:
  - name: "线性规划(LP)"
    rationale: "目标函数和约束均为线性，问题规模适中"
    complexity: "O(n)"
    pros: ["求解速度快", "有全局最优解保证"]
    cons: ["无法处理非线性关系"]
  - name: "遗传算法(GA)"
    rationale: "作为对比方法"
    complexity: "O(g·p·n)"
    pros: ["全局搜索", "不要求可微"]
    cons: ["收敛慢", "结果不稳定"]

selected_model: "线性规划(LP)"
selection_reason: "问题线性性强，优先选择可解释性高、求解稳定的方法"

## 2. 验证策略
validation_method: "cross_validation"  # 或 holdout / bootstrap / sensitivity
metrics:
  - name: "R²"
    threshold: 0.7
    interpretation: "模型解释的方差比例"
  - name: "MAE"
    threshold: 0.1
    interpretation: "平均绝对误差"
baseline: "均值预测"  # 最简单的基准方法

## 3. 数据需求
required_data:
  - variable: "X1"
    description: "自变量1描述"
    source: "问题附件/公开数据/模拟生成"
    expected_range: [0, 100]
  - variable: "Y"
    description: "因变量描述"
    source: "问题附件"

## 4. 失败预案
if_model_fails:
  primary_fallback: "尝试对数变换后重新回归"
  secondary_fallback: "切换到随机森林回归"
  give_up_condition: "R² < 0.05 且所有变换无效"
  honest_report: "如实报告模型预测能力有限，改用分组策略"

## 5. 可复现性要求
reproducibility:
  seed: 42
  environment: "Python 3.11 + scikit-learn 1.3"
  data_version: "v1.0 (原始附件)"
```

---

## 依赖图 (Dependency Graph)

模型间的依赖关系通过 `depends_on` 字段声明，形成 DAG：

```
示例 DAG:
  model_1 (独立) ─────────────────┐
                                   ├──> model_4 (综合模型)
  model_2 (独立) ──> model_3 ──────┘
```

规则：
- `depends_on: []` 表示独立模型，可以并行构建
- `depends_on: ["model_2"]` 表示必须等 model_2 完成才能开始
- 不允许循环依赖（pipeline_manager 自动检测）

---

## 分数轨迹追踪 (Score Trajectory)

每个阶段完成后，记录质量分数到 `pipeline.json` 的 `score_trajectory` 数组：

```json
{
  "stage": "model_1_verify",
  "timestamp": "2026-05-24 10:30:00",
  "metrics": {
    "R²": 0.85,
    "MAE": 0.072,
    "formulation_score": 90,
    "code_quality_score": 85
  },
  "passed": true,
  "reworks": 0
}
```

目的：追踪全流程质量变化，识别薄弱环节。

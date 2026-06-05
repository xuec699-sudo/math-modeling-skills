# 数学建模竞赛 QA 检查清单 v4.0

> **来源**: KyrieZhang329/MathModeling-skills QA Checklist + 本技能定制
> **用法**: 终稿组装前逐项检查。任一 `failed` 阻断终稿。
> **输出**: `paper/qa_report.md`

---

## 一、最终决策

三种 QA 状态：

| 状态 | 含义 | 后续动作 |
|------|------|---------|
| `passed` | 全部通过 | 允许终稿组装 |
| `passed_with_warnings` | 通过但有注意事项 | 允许组装，但局限性需保持可见 |
| `failed` | 阻断 | 禁止组装，修复最早的阻断项 |

---

## 二、工作流完整性（所有子问题必须通过）

对每个子问题 Qx：

- [ ] 候选方法池存在 (`methods/Qx/qx_method_candidates.md`)
- [ ] 实验报告存在 (`results/Qx/experiments/roundN/`)
- [ ] 方法迭代日志存在 (`methods/Qx/qx_method_iteration_log.md`)
- [ ] **最终方法说明存在** (`methods/Qx/qx_final_method_explanation.md`) ★ 规则1
- [ ] **最终结果分析存在** (`results/Qx/reports/qx_final_result_analysis.md`) ★ 规则2
- [ ] **求解方案包存在** (`results/Qx/reports/qx_solution_package_for_writer.md`) ★ 规则3
- [ ] 鲁棒性报告存在 (`robustness/Qx/qx_robustness_report.md`) 或有合理豁免
- [ ] 图表计划存在 (`methods/Qx/qx_figure_table_plan.md`)
- [ ] **冻结数值存在** (`frozen/Qx/frozen_numbers.json`) ★ 规则4 (v4.0新增)

---

## 三、问题覆盖

- [ ] 每个原始子问题已列出
- [ ] 每个子问题有对应回答
- [ ] 每个回答有模型、结果或有理由的非模型回答
- [ ] 子问题间依赖关系已处理
- [ ] 最终结论映射回原题

**阻断项**：缺子问题 / 曲解子问题 / 结论未回答所提问题

---

## 四、方法一致性

- [ ] 任务类型与方法匹配（分类问题不用回归，评价问题不用预测）
- [ ] 论文方法描述与最终方法说明一致（非早期候选池）
- [ ] 每个主模型有基线对比（除非有合理豁免）
- [ ] 改进模型明确标注为"可选"
- [ ] 淘汰的方法在适当位置提及
- [ ] **PoC存在**: 每个候选方法有 ≤30行概念验证代码 ★ (v4.0新增)

---

## 五、数据一致性

- [ ] 原始数据未改动
- [ ] 清洗数据有文档
- [ ] 字段含义和单位清晰
- [ ] 缺失值和异常值已处理或讨论
- [ ] 脚本使用的数据与数据报告一致

---

## 六、代码与结果一致性

- [ ] 脚本存在于 `code/Qx/` 下
- [ ] 运行说明存在
- [ ] 输出文件遵循 `experiments/roundN/` 结构
- [ ] `run_summary.json` 每轮存在
- [ ] **论文数值与冻结数值一致** ★ (v4.0新增)
- [ ] 随机种子已固定
- [ ] 论文中的数字可在输出文件中找到

---

## 七、基线对比与鲁棒性

- [ ] 基线结果存在
- [ ] 主模型与基线已对比
- [ ] 鲁棒性或敏感性检查每子问题存在
- [ ] 脆弱结论已标注
- [ ] 结论边界已陈述

---

## 八、图表

- [ ] 每张引用的图存在
- [ ] 每张引用的表存在
- [ ] 每张图/表有来源产物
- [ ] 论文图为 Type 3（论文图），非 Type 1（诊断图）
- [ ] 图注解释核心发现
- [ ] 视觉证据支持相关声明

---

## 九、论文字数与质量 (v4.0)

- [ ] 每节达到 G5.1 字数下限（见 paper-writing-rules.md）
- [ ] 每个数值结果达到 G5.2 三维讨论（≥3维度）
- [ ] 总字数 15,000-22,000
- [ ] 模型构建部分 ≥ 总字数 35%
- [ ] 无 AI 填充语过度使用
- [ ] 公式渲染正确（OMML 验证通过）

---

## 十、模型建立质量 (v4.0)

- [ ] 每个子问题明确声明模型类型
- [ ] 符号表完整（符号/含义/单位/类型）
- [ ] 假设区分为必要假设和简化假设
- [ ] 物理模型有完整推导链（物理定律->公式）
- [ ] 优化模型有：决策变量+目标函数+约束条件
- [ ] 参数取值有来源依据

---

## 十一、反编造

- [ ] 无编造数据、参考文献、结果、图表、实验
- [ ] 无编造数值
- [ ] 无无证据的优越性声明
- [ ] 无隐藏的不确定性

---

## 十二、产物可追溯性

每个主要声明至少对应一个支持产物：

| 声明类型 | 期望产物 |
|---------|---------|
| 问题理解 | problem_parse.json |
| 方法选择 | final_method_explanation.md |
| 数据声明 | data_report.md |
| 数值结果 | frozen_numbers.json + run_summary.json |
| 图表声明 | 图源文件 + figure_table_plan.md |
| 鲁棒性声明 | robustness_report.md |
| 最终结论 | 论文节 + 对应结果文件 |

找不到产物 → 移除声明或标注不完整。

---

## 十三、修复路由表

使用最早能修复问题的 skill：

| 问题 | 修复 skill |
|------|-----------|
| 问题理解错误 | problem_analysis (pipeline stage) |
| 任务类型选错 | problem-classifier → model-formulation-guide.md |
| 方法与任务/数据不匹配 | method-selector → references/problem-algorithm-map.json |
| 跨子问题符号冲突 | 符号表统一 (quality_gate.py) |
| 缺失或矛盾的假设 | model-formulation-guide.md sec 1.1 |
| 数据问题 | data_preprocessing (pipeline stage) |
| 缺失方法说明 (规则1) | model_build (pipeline stage) |
| 缺失结果分析 (规则2) | model_verify (pipeline stage) |
| 缺失求解包 (规则3) | paper_write (pipeline stage) |
| 冻结数值漂移 (规则4) | frozen_numbers.py defrost → freeze |
| 代码与输出不一致 | model_verify (pipeline stage) |
| 缺失鲁棒性证据 | sensitivity_analysis (pipeline stage) |
| 缺失或低质量图表 | plot_figures_nature.py / draw_image.py |
| 文字问题或过度声明 | paper_review (pipeline stage) |
| 公式渲染失败 | build_docx.py validate |
| 多项阻断 | pipeline_manager.py status → 逐项修复 |
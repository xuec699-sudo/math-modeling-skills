# 学术诚信验证闸门 (Integrity Gate)

> **位置**: pipeline stage `integrity_gate`，位于 `content_assembly` 之后、`paper_review` 之前。
> **来源**: 基于 ARS academic-pipeline Stage 2.5 的 7 类阻断式检查清单，适配数模竞赛场景。
> **执行时机**: 论文内容撰写完成后，提交同行评审前。

---

## 阻断式检查清单 (7 类)

凡标记 **HARD FAIL** 的项目，必须修复后才能通过闸门。

### 1. 引用真实性 (Citation Integrity)
| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 每一条参考文献是否真实存在？ | HARD FAIL | 通过 Semantic Scholar / CrossRef API 验证 DOI/标题 |
| 引用是否确实支撑文中主张？ | HARD FAIL | 检查引用处的 claim 与被引文献的实际内容是否一致 |
| 是否存在自引过度（>30% 引用来自同一作者组）？ | WARN | |
| 引用格式是否统一？ | WARN | |

### 2. 数据真实性 (Data Integrity)
| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 数据来源是否可追溯？ | HARD FAIL | 每条数据必须注明出处或生成方式 |
| 是否存在不可能的数据范围？ | HARD FAIL | 如概率 >1、负的人口数等 |
| 数据量是否足够支撑模型复杂度？ | WARN | 样本量 < 特征数 × 10 时警告 |
| 数据预处理步骤是否完整记录？ | WARN | |

### 3. 模型正确性 (Model Correctness)
| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 模型公式是否数学上成立？ | HARD FAIL | 维度一致性、定义域检查 |
| 参数是否有合理取值范围？ | HARD FAIL | 不能有无物理意义的参数值 |
| 优化模型是否包含完整约束？ | HARD FAIL | |
| 假设是否与模型方法一致？ | WARN | 如用 OLS 但未检验线性性 |

### 4. 统计有效性 (Statistical Validity)
| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 假设检验的 p 值是否合理？ | HARD FAIL | p=0.000 需要注明是近似值 |
| 置信区间是否被报告？ | WARN | |
| 多重比较是否做了校正？ | WARN | |
| 样本量是否满足统计功效要求？ | WARN | |

### 5. 结果一致性 (Result Consistency)
| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 摘要/结论中的数值与正文是否一致？ | HARD FAIL | 数字交叉验证 |
| 图表数据与正文描述是否一致？ | HARD FAIL | |
| 模型间的结论是否矛盾？ | HARD FAIL | 如模型1说正相关，模型2说负相关且未解释 |

### 6. 逻辑完整性 (Logical Completeness)
| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 每个子问题的结论是否有对应的模型支撑？ | HARD FAIL | |
| 灵敏度分析的参数范围是否合理？ | WARN | |
| 模型的局限性是否被讨论？ | WARN | 缺少 Limitations 段落 |

### 7. 表述规范性 (Expression Standards)
| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 模型类型是否明确声明？ | HARD FAIL | 不能只说"建立了数学模型" |
| 所有变量是否有符号表？ | HARD FAIL | |
| 公式是否有编号？ | WARN | |
| 图表是否有标题和编号？ | WARN | |

---

## 闸门通过条件

- **PASS**: 0 个 HARD FAIL + WARN ≤ 5
- **REWORK**: 有 HARD FAIL → 修复后重新检查
- **MAX CYCLES**: 3 轮未通过 → 人工介入

## 与其他闸门的关系

- `quality_gate.py` (depth/formula/figure_ctx): 格式层检查，在 `content_assembly` 末尾执行
- `integrity_gate`: 内容层检查，在 `integrity_gate` 阶段执行
- `paper_review`: 第三方评审，在 `paper_review` 阶段执行

三层递进：格式 → 内容完整性 → 同行评审
# 结果溯源性检查 (Result Traceability) — v5.2 新增

> **来源**: math-modeling-competition-workflow — 论文中每个数字都必须可追溯到代码输出

## 铁律 (IRON RULE)

**论文中的每一个数字，必须满足以下三条之一：**

1. **由代码产出** — 数字直接来自 un_summary.json、esults/ 目录下的输出文件、或代码生成的图表
2. **来自官方来源** — 数字来自题目附件、竞赛规则、或标注的公开数据
3. **标注为假设** — 数字是模型假设值，且已明确标注"本文假设..."

**违反任一情况 = HARD FAIL，论文不得通过闸门。**

## 逐项检查清单

| 检查项 | 严重性 | 验证方法 |
|--------|--------|----------|
| 摘要中每个数值是否能在正文/图表中找到对应？ | HARD FAIL | 逐数字反向搜索 |
| 正文中每个数值是否能追溯到代码输出文件？ | HARD FAIL | 数字 → 产物映射表 |
| 所有图表中的数据是否由脚本生成（非手动填入）？ | HARD FAIL | 检查图源文件时间戳 |
| 是否存在"凭空出现"的百分比或精度值？ | HARD FAIL | 全文搜索%和数字，逐一溯源 |
| 模型性能指标(R²/MAE/AUC等)是否来自 un_summary.json？ | HARD FAIL | 交叉验证 |
| 假设参数值是否标注"假设"且有合理依据？ | WARN | |

## 数字溯源映射表模板

论文撰写时，agent 必须维护以下映射表（写入 CUMCM_Workspace/memory/number_trace.md）：

| 论文位置 | 数值 | 含义 | 来源文件 | 是否已验证 |
|----------|------|------|----------|-----------|
| 摘要第3句 | 94.7% | 分类准确率 | results/Q3/test_metrics.json | ✅ |
| 表4 | 2.34 | RMSE | results/Q2/error_analysis.csv | ✅ |
| 图3 | - | 收敛曲线 | results/figures/Q1_convergence.png | ✅ |
| §5.2 第2段 | λ=0.01 | 正则化系数 | 模型假设 | ⚠️ 假设值 |

## 图表三段论强制规则

每张图/表在正文中必须配有：

1. **描述 (Description)**: 图表展示了什么内容
2. **分析 (Analysis)**: 观察到了什么模式/对比/趋势
3. **结论 (Conclusion)**: 由此得出什么决策或答案

**缺失任何一环 = WARN**，累计3个WARN = HARD FAIL。

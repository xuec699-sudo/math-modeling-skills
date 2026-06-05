<p align="center">
  <img src="assets/icon-large.svg" alt="Math Modeling Contest" width="120"/>
</p>

<h1 align="center">Math Modeling Contest Agent</h1>

<p align="center">
  <strong>v5.3.3</strong> · 工业级数学建模竞赛全流程 Agent
</p>

<p align="center">
  <img alt="Codex" src="https://img.shields.io/badge/Codex-supported-339cff">
  <img alt="CUMCM" src="https://img.shields.io/badge/竞赛-国赛%20CUMCM-1A6FC4">
  <img alt="MCM" src="https://img.shields.io/badge/竞赛-美赛%20MCM%2FICM-E28E2C">
  <img alt="51MCM" src="https://img.shields.io/badge/竞赛-五一赛%2051MCM-2E9E44">
  <img alt="Version" src="https://img.shields.io/badge/version-5.3.3-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

---

> 从赛题到终稿，一站式交付。双模式运行、六维选题评估、模型依赖 DAG、五人评审团、学术诚信门控、公式自动渲染——把数学建模竞赛变成可追溯、可审计的工程流水线。

## 为什么需要这个？

建模竞赛真正失败的地方，往往不是"不会模型"，而是**流程漂移**：
- 题没读清楚就上复杂模型
- 论文里写的数字脚本输出找不到
- bug 修复后论文数字偷偷漂移没人察觉

`math-modeling-contest` 把这些漂移模式做成"结构上藏不住"的形态——每个数字可追溯、每次修改有审计、每项声明有证据。

## 核心能力

| 能力 | 说明 |
|---|---|
| **双模式运行** | Autopilot（全自动管道）或 Manual（人工强制检查点） |
| **六维选题评估** | 从数据可得性、建模难度、创新空间等 6 个维度评估选题 |
| **L3+ 模型推导深度** | 强制达到工程可复现的推导深度，拒绝"显然可得" |
| **模型依赖 DAG** | 子模型间的依赖关系可视化为有向无环图 |
| **五人评审团** | 5 个独立 reviewer 打分，≥65 分才放行 |
| **学术诚信门控** | 7 类阻断式检查（抄袭、数据造假、引用缺失等） |
| **公式自动渲染** | LaTeX → OMML 原生 Word 公式（可编辑，非图片） |
| **三线表自动排版** | 国赛标准三线表，一键生成 |
| **分数轨迹追踪** | 每次修改后自动追踪论文质量分数变化 |
| **18-22 页标准输出** | 符合国赛/美赛页数规范，自动内容量检查 |

## 运行模式

### Autopilot 模式
```bash
python scripts/pipeline_manager.py auto
```
全自动跑完：分析 → 建模 → 验证 → 论文。适合快速原型和 deadline 冲刺。

### Manual 模式
```bash
python scripts/pipeline_manager.py manual
```
每个阶段有显式门控（enter_condition / pass_criteria / fail_fallback），失败会标脏下游产物。适合追求可控性和质量。

## 支持的竞赛

| 竞赛 | 语言 | 论文格式 |
|---|---|---|
| **CUMCM** 全国大学生数学建模竞赛（国赛） | 中文 | 三线表、宋体+黑体、A4 |
| **51MCM** 五一数学建模竞赛 | 中文 | 三线表、宋体+黑体、A4 |
| **MCM/ICM** 美国大学生数学建模竞赛（美赛） | 英文 | 标准学术格式 |

## 快速开始

### 安装

```bash
# 安装到 Codex
codex skills install github.com/xuec699-sudo/math-modeling-skills
```

或手动复制 `SKILL.md` 所在目录到 `$CODEX_HOME/skills/math-modeling-contest/`。

### 使用

在 Codex 中说：
- "求解这道题" / "solve this" — 全流程跑
- "只做问题1" — 分段执行
- "生成论文" / "write paper" — **强制走 `build_docx.py`**（非 Pandoc）
- "修改论文" / "revise paper" — **原地编辑 DOCX**
- "审阅论文" — QA 清单检查

### 论文生成（关键流程）

```bash
# 1. 写 Markdown 草稿（LaTeX 公式 + [FIGURE:] 占位符）
# 2. 一键生成 DOCX
python scripts/build_docx.py draft.md output.docx
# 3. 如果内容不足 15000 字 → HARD FAIL → 扩展后重试
```

> ⚠️ **严禁**使用 Pandoc 或手动 `python-docx` 绕过此流程。

## 项目结构

```
math-modeling-contest/
├── SKILL.md                    # 核心技能定义（45KB）
├── agents/                     # Agent 配置
├── scripts/                    # 核心脚本（60+ 个）
│   ├── pipeline_manager.py     # 管道编排器（30KB）
│   ├── quality_gate.py         # 质量门控（51KB）
│   ├── build_docx.py           # DOCX 生成器（LaTeX→OMML）
│   ├── plot_figures_nature.py  # 论文级图表生成
│   ├── model_remediator.py     # 模型修复器
│   └── ...
├── references/                 # 参考文档
│   ├── algorithm-library/      # 7 类算法库（优化/预测/评价/图论/统计/综合/ML）
│   ├── role-guides/            # 建模手/编程手/论文手角色指南
│   ├── problem-triage.md       # 六维选题评估
│   ├── integrity_gate_checklist.md  # 学术诚信 7 类检查
│   ├── model-formulation-guide.md   # 模型建立指南
│   └── ...
└── templates/                  # 论文模板（LaTeX + DOCX）
```

## 许可证

MIT License

---

<p align="center">
  <sub>Built for CUMCM · 51MCM · MCM/ICM</sub>
</p>

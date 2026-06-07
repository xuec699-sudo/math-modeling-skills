<p align="center">
  <img src="assets/icon-large.svg" alt="Math Modeling Contest" width="120"/>
</p>

<h1 align="center">Math Modeling Contest Agent</h1>

<p align="center">
  <strong>v5.8.1</strong> · 工业级数学建模竞赛全流程 Agent
</p>

<p align="center">
  <img alt="Codex" src="https://img.shields.io/badge/Codex-supported-339cff">
  <img alt="CUMCM" src="https://img.shields.io/badge/竞赛-国赛%20CUMCM-1A6FC4">
  <img alt="MCM" src="https://img.shields.io/badge/竞赛-美赛%20MCM%2FICM-E28E2C">
  <img alt="51MCM" src="https://img.shields.io/badge/竞赛-五一赛%2051MCM-2E9E44">
  <img alt="Version" src="https://img.shields.io/badge/version-5.8.1-blue">
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
| **Friendly Mode** | 关键决策用编号选项推进，用户不用手敲命令或编辑 JSON |
| **三角色协作** | 建模手、编程手、论文手职责分离，交接依赖可追溯 |
| **状态日志** | 长流程可维护 `state/decision_log.json`，中途恢复不丢上下文 |
| **六维选题评估** | 从数据可得性、建模难度、创新空间等 6 个维度评估选题 |
| **L3+ 模型推导深度** | 强制达到工程可复现的推导深度，拒绝"显然可得" |
| **模型依赖 DAG** | 子模型间的依赖关系可视化为有向无环图 |
| **五人评审团** | 5 个独立 reviewer 打分，≥65 分才放行 |
| **学术诚信门控** | 7 类阻断式检查（抄袭、数据造假、引用缺失等） |
| **公式自动渲染** | LaTeX → OMML 原生 Word 公式（可编辑，非图片） |
| **三线表自动排版** | 国赛标准三线表，一键生成 |
| **分数轨迹追踪** | 每次修改后自动追踪论文质量分数变化 |
| **实质内容下限** | 9000 字以下硬拦截；9000 字以上按问题复杂度自然展开，不强行凑字数 |

## 设计吸收点

这版参考了两个优秀开源 skill 的思路，但没有复制文本或文件：

- [`handsomeZR-netizen/mathmodel-skill`](https://github.com/handsomeZR-netizen/mathmodel-skill)：吸收“编号问答式 Friendly Mode、状态日志、分层反馈、竞赛特化”的设计思想。
- [`XiaoMaColtAI/math-modeling-skill`](https://github.com/XiaoMaColtAI/math-modeling-skill)：吸收“三角色协作、算法库索引、Figure Contract、Claim-Evidence 写作”的组织思路。

本项目仍保留自己的主架构：G1-G6 门控、结果冻结、质量审计、`build_docx.py` 原生 Word 生成，以及 9000 实质字符下限。

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

## 不知道怎么调用？直接复制这些提示词

安装完成后，不需要手动运行 `SKILL.md`。你只要在 Codex 里明确提到 `math-modeling-contest`，或者直接描述“数学建模竞赛 / 国赛 / 美赛 / 五一赛 / CUMCM / MCM / ICM”，Codex 就会读取这个 skill 并按里面的流程工作。

### 最推荐的首次启动提示词

```text
请使用 math-modeling-contest skill 帮我完成这道数学建模竞赛题。
竞赛类型：国赛/CUMCM
运行模式：先 Manual，不要直接写论文，每一步先给我门控检查结果。
我会把题目文件、附件数据和已有代码发给你。
请先完成：读题、问题拆解、数据检查、建模路线选择，并告诉我下一步该做什么。
```

### 完整赛题一键启动示例

如果你已经把赛题 PDF/Word 和附件数据上传给 Codex，可以直接复制下面这段：

```text
请使用 math-modeling-contest skill 完整求解我上传的数学建模赛题。

赛题文件：我已上传题目 PDF/Word
附件数据：我已上传所有 Excel/CSV/图片/说明文件
竞赛类型：国赛/CUMCM（如果你判断不是国赛，请先说明）
运行模式：Manual checkpoint 模式

请按下面顺序执行：
1. 读取赛题和全部附件，先不要写论文。
2. 输出问题拆解：每一问的输入、输出、约束、评价指标、依赖关系。
3. 检查数据质量：缺失值、异常值、单位、字段含义、是否需要派生变量。
4. 给每一问提供 2-3 个候选模型，并说明优缺点、数据需求、最小 PoC 验证方案。
5. 建立模型依赖 DAG，说明哪些子问题可以并行，哪些必须等待前置结果。
6. 等我确认路线后，再进入代码求解、图表生成、论文初稿和 DOCX 输出。

硬性要求：
- 论文数字必须能追溯到脚本输出。
- 每个模型必须有变量表、公式、约束或核心方程。
- 每个关键结果必须有图表解释和鲁棒性/敏感性分析。
- 生成论文时必须使用 scripts/build_docx.py，不要用 Pandoc。
- 论文只设 9000 个实质字符下限，不要为了达到某个字数目标而填充废话。
```

如果你想让它全自动推进，把“运行模式”改成：

```text
运行模式：Autopilot，全流程自动推进；但每完成一个大阶段请给我一次简短状态汇报。
```

### 如果你想全自动推进

```text
请使用 math-modeling-contest skill，按 Autopilot 模式求解这道题。
要求：从题目解析、建模、代码、结果验证、图表、论文初稿到最终审阅都走完整流程。
每个阶段必须留下可追溯文件，论文中的数字必须能追溯到脚本输出。
```

### 如果你只想做其中一问

```text
请使用 math-modeling-contest skill，只处理问题 1。
先判断这是预测、优化、评价、机理建模还是综合类问题。
然后给出 2-3 个候选模型，每个模型都要有优缺点、数据需求和最小 PoC 验证方案。
```

### 如果你已经有论文初稿，只想修改

```text
请使用 math-modeling-contest skill 修改我的已有 DOCX 论文。
注意：不要从 Markdown 重新生成整篇论文，必须用 in-place edit 的方式在原文档基础上修改。
我会说明要改的段落、表格或图。
```

### 如果 skill 没有自动触发

把第一句话写得更明确：

```text
Use the math-modeling-contest skill. Read its SKILL.md first, then follow its gate-driven workflow.
```

或者中文：

```text
请显式调用 math-modeling-contest 这个 skill，先读取 SKILL.md，再按 G1-G6 门控流程执行。
```

### 本地手动安装方式

如果 `codex skills install` 不可用，可以手动安装：

```bash
git clone https://github.com/xuec699-sudo/math-modeling-skills.git math-modeling-contest
```

然后把整个 `math-modeling-contest/` 文件夹放到你的 Codex skills 目录中，例如：

```text
$CODEX_HOME/skills/math-modeling-contest/
```

目录里必须能直接看到：

```text
math-modeling-contest/
├── SKILL.md
├── scripts/
├── references/
└── templates/
```

### 论文生成（关键流程）

```bash
# 1. 写 Markdown 草稿（LaTeX 公式 + [FIGURE:] 占位符）
# 2. 一键生成 DOCX
python scripts/build_docx.py draft.md output.docx
# 3. 如果实质内容不足 9000 字 → HARD FAIL → 只补充推导、对比、鲁棒性和图表解释后重试
```

> ⚠️ **严禁**使用 Pandoc 或手动 `python-docx` 绕过此流程。

## 项目结构

```
math-modeling-contest/
├── SKILL.md                    # 精简后的核心执行规则（约 10KB）
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

维护原则：`SKILL.md` 只保留触发后必须执行的核心流程；长示例、算法细节、格式规范和审计清单放在 `references/`，避免主入口过长或重复。

## 许可证

MIT License

---

<p align="center">
  <sub>Built for CUMCM · 51MCM · MCM/ICM</sub>
</p>


## v5.7.0 Gate Contracts & Audit Layer

### New: G1-G6 Gate Contracts
Explicit enter_condition / pass_criteria / fail_fallback for every workflow checkpoint.
Run: `python scripts/quality_gate.py contracts`

| Gate | Purpose |
|------|---------|
| G1 PROBLEM_PARSED | Problem parsed + classified + literature searched |
| G2 METHOD_VALIDATED | Every candidate has <=30-line PoC with feasibility number |
| G3 CODE_REVIEWED | Code review with >=5 disk file items |
| G4 RESULTS_FROZEN | frozen_numbers.json not stale; 3-step refreeze protocol |
| G5 PAPER_SECTION_READY | Word count + >=3 discussion dimensions per result |
| G6 AUDIT_LAYER_PASSED | 3 independent auditors ALL must PASS |

### New: P1 Change Propagation Rule
After modifying code/methods/results/planning files, grep workspace for stale references.
Run: `python scripts/quality_gate.py propagate --changed-files ...`

### New: G2 PoC Hard Gate
Every candidate method requires <=30-line PoC script with feasibility result.
Run: `python scripts/quality_gate.py g2_poc`

### New: G4 Frozen Staleness Detection
Auto-detects when source files are newer than frozen_numbers.json, marks as STALE.
Run: `python scripts/quality_gate.py g4_stale`

### New: G6 Enhanced Independent Audit Layer
Three orthogonal auditors with mandatory disk artifacts:
- Consistency audit -> `paper/audits/cross_media_consistency_audit.md`
- Completeness audit -> `paper/audits/completeness_audit.md`
- Quality audit -> `paper/qa_report.md`

Run: `python scripts/quality_gate.py g6_audit`

### New: frozen_numbers.py re-freeze command
Three-step protocol: thaw (log reason) -> modify (update source) -> re-freeze.
Run: `python scripts/frozen_numbers.py re-freeze --subquestion Q1`

### New: Environment Ping
Session-start checks: git status, Python version, scientific packages, workspace skeleton.

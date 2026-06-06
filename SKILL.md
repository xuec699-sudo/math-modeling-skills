---
name: math-modeling-contest
description: >
  Industrial-grade math modeling contest agent for CUMCM (国赛), 51MCM (五一赛),
  and MCM/ICM (美赛). Supports dual-mode operation: Autopilot (AI-driven full
  pipeline) or Manual (human-spec-led with mandatory checkpoints). Use when the
  user needs to solve a math modeling contest problem end-to-end, mentions CUMCM,
  51MCM, MCM, ICM, 数学建模, 国赛, 美赛, or asks to build a mathematical model
  for a competition problem. v2.0 adds deep-research literature search, experiment
  design framework, academic integrity gate, 5-reviewer panel with score >=65,
  model dependency DAG, score trajectory tracking, and writing anti-pattern detection.
metadata:
  version: "5.7.1"
  short-description: Math modeling contest v5.7.1 - G1-G6 gate contracts + PoC hard gate + frozen staleness detection + P1 change propagation + independent 3-layer audit + baseline-first modeling + figure D-A-C rule + abstract template + LaTeX verification + L3+ model derivation depth + result traceability + 9000-char substantive floor
---

# Math Modeling Contest Agent v5.7.1

---

## Open-Source Quick Start

When a user provides a math modeling contest problem, first decide whether this is a new solution or a revision of an existing DOCX:

- New contest solution: parse the problem, inspect attachments, design models, run code, verify results, write Markdown, then generate DOCX with `scripts/build_docx.py`.
- Existing DOCX revision: edit the DOCX in place with `python-docx`; do not regenerate the whole paper unless the user explicitly asks.

Use Manual mode when the user wants checkpoint control. Use Autopilot only when the user explicitly asks for full automatic execution.

Minimum paper content rule: require at least 9,000 substantive Chinese characters. There is no artificial upper limit and no fixed character-count target. Never add filler to chase length.

## Canonical Workflow

This section is the source of truth for using the skill. If later legacy notes conflict with this section, follow this section first.

1. Intake: identify contest type, uploaded files, requested mode, and whether this is a new paper or a DOCX revision.
2. G1 Problem Parsed: split every subproblem into inputs, outputs, constraints, objective functions, evaluation metrics, and dependencies.
3. G2 Method Validated: provide at least two candidate methods for each subproblem, then run a minimal PoC or baseline before committing to a complex model.
4. G3 Code Reviewed: implement reproducible scripts with fixed seeds, explicit input/output paths, and traceable result files.
5. G4 Results Frozen: freeze all numbers, tables, and figures before writing. If data or code changes, refreeze the results before editing the paper.
6. G5 Paper Section Ready: write the Markdown draft only after verified results exist. Every figure/table should follow the D-A-C rule: describe, analyze, conclude.
7. G6 Audit Layer Passed: check citations, data provenance, formulas, statistics, consistency, unsupported claims, and Word rendering.
8. Deliver: generate DOCX with `scripts/build_docx.py`, then verify editable OMML formulas, figures, tables, captions, layout, and Markdown cleanup.

Core routing rules:

- New contest solution: Markdown draft -> `scripts/build_docx.py` -> DOCX.
- Existing DOCX revision: use `python-docx` for in-place editing; do not rebuild the whole paper unless the user explicitly asks.
- Length: 9,000 substantive Chinese characters is a hard minimum only. There is no upper limit and no target length. Expand only with evidence-bearing derivations, baselines, sensitivity analysis, error analysis, preprocessing details, and figure/table interpretation.
- Language and labels: CUMCM/51MCM use Chinese; MCM/ICM use English.
- Figures: prefer the Nature-style figure logic from `nature-figure`: define the communication goal first, choose a clean multi-panel structure when useful, keep labels readable, and make every visual support a concrete claim.

## Contributor Cleanup Note

Keep `SKILL.md` focused on operational rules. Move long examples, formatting references, and contest-specific appendices into `references/` when possible. Avoid duplicated frontmatter, repeated workflow blocks, or garbled text in newly added sections.

## Format Standard

Based on `templates/2026建模竞赛A题_最终论文.docx`.

All generated papers MUST follow the reference template:

| Element | Font | Size | Weight | Align |
|---------|------|:----:|:------:|:-----:|
| Title | 黑体 | 16pt | Bold | Center |
| Heading 1 | 黑体 | 14pt | Bold | Center |
| Heading 2 | 黑体 | 13pt | Bold | Left |
| Heading 3 | 黑体 | 12pt | Bold | Left |
| Body (Chinese) | 宋体 | 12pt (小四) | Normal | Justify, 1.5x line spacing |
| Body (English/digits) | Times New Roman | 12pt | Normal | - |
| Table header | 宋体+TNR | 10.5pt (五号) | Bold | Center |
| Table data | 宋体+TNR | 10.5pt (五号) | Normal | Center |
| Table caption | 黑体 | 10.5pt | Bold | Center, ABOVE table |
| Figure caption | 黑体 | 10.5pt | Bold | Center, BELOW figure |
| Code | Consolas | 10.5pt | Normal | Left |

**Page:** A4 (21.0 x 29.7 cm), margins: top/bottom 2.5cm, left/right 3.2cm

**Tables:** Three-line format (top 1.5pt, bottom 1.5pt, header underline 0.75pt). No vertical lines. No horizontal lines between data rows.

**Indent:** Body paragraphs: first-line indent 0.74cm (2 characters).

PAPER GENERATION - MANDATORY WORKFLOW (READ FIRST)

**论文操作分两条路径，先判断再执行：**

`
用户请求
  ├── 生成论文/写论文/首次求解 → 走路径A：Markdown → build_docx.py（新建）
  └── 修改论文/改一下/调整XX   → 走路径B：python-docx 原地编辑（禁止重建）
`

## 路径 B：修改已有论文 —— IN-PLACE EDIT（优先判断）

**如果用户已有 .docx 初稿且要求修改，必须走此路径，禁止走路径A！**

1. 用 python-docx 打开原 DOCX
2. 定位到需修改的段落/表格/图片
3. 直接编辑 → 保存为新版本（xxx_v2.docx, xxx_v3.docx...）
4. 告知用户：改了哪里、保存到哪个文件

## 路径 A：首次生成论文

**仅在以下情况走此路径：① 首次求解赛题 ② 用户明确说重新生成 ③ 没有已存在的 DOCX**

**When generating a NEW paper, follow these steps IN ORDER:**

### Step 0: Follow Nature-Style Writing Standards

**Before writing any section, consult `references/nature-writing-guide.md`** for anti-AI writing patterns:

- No vague claims ("显著提高") without baselines
- No formulaic openings ("本文针对...建立了...")
- Challenge → Contribution → Evidence structure
- One message per paragraph, topic sentence first
- Claims bounded by evidence; results separated from implications

### Step 1: Write a complete Markdown draft
- Use double-dollar for display equations, single-dollar for inline math
- Use [FIGURE: filename.png | Figure X Title] for figures (Chinese title for CUMCM/51MCM, English for MCM/ICM)
- Table caption: put "**表N 标题**" on the line BEFORE the table (or [表题] placeholder appears)
- Table body: use standard Markdown | col1 | col2 | then |---|---|
- Hard minimum: 9,000 substantive Chinese characters. There is no artificial upper/target length.
- Let the final length follow the problem depth, data volume, derivations, experiments, and result interpretation.
- If under the hard minimum, expand only evidence-bearing content: derivations, baseline comparison, robustness/sensitivity, error analysis, data preprocessing details, and figure/table D-A-C interpretation.
- FORBIDDEN: padding with generic background, repeated problem statements, empty "significance" prose, or unsupported claims just to reach a character count.
- Each sub-problem model chapter MUST have >= 2,000 chars
- Each sub-problem MUST have >= 3 equations

### Step 2: Generate DOCX with build_docx.py (NO EXCEPTIONS)
`
python scripts/build_docx.py draft.md output.docx
`
This ONE command handles ALL formatting automatically (including #### heading cleanup, --- separator removal,  `  fence skipping):
- All LaTeX equations become Word native OMML (editable, NOT pictures)
- All [FIGURE:] placeholders become embedded PNG images with captions
- All markdown tables become CUMCM three-line tables
- Content length check: under 9,000 chars = HARD FAIL; 9,000+ chars = PASS with no artificial length target
- Markdown cleanup: bold/italic markers, list bullets, blockquotes, inline code, and links are stripped before DOCX output
- Fonts: SimSun body + SimHei headings + Times New Roman English
- Page: A4, 2.54cm/3.17cm margins

### Step 3: If HARD FAIL, expand with evidence
- Do NOT bypass with Pandoc, python-docx, or manual scripts
- If HARD FAIL (<9,000 chars), expand before delivery.
- Expand model chapters only with traceable content: formula derivation, algorithm steps, baseline results, sensitivity analysis, uncertainty/error discussion, and figure/table interpretation.
- Never add filler merely to satisfy a character count.
- Retry build_docx.py until it passes

### FORBIDDEN PATHS (DO NOT USE)
- pandoc paper.md -o paper.docx
- Manual Document() + add_paragraph()
- Any workflow that skips build_docx.py content check

---


### LaTeX 编译验证清单 (v5.6 —— 集成自 math-modeling-competition-workflow)

**每次 LaTeX 编译后必须逐项检查：**

| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 编译至少两次 | HARD FAIL | 交叉引用需要两次编译才能正确解析 |
| 无 fatal error | HARD FAIL | 任何 ! 开头的 fatal error 必须修复 |
| 无 undefined references | HARD FAIL | 所有 \ref{} 和 \cite{} 必须解析 |
| 无 multiply-defined labels | HARD FAIL | 跨页 longtable 检查 \endfirsthead |
| 无 missing figures | HARD FAIL | 所有 \includegraphics 路径必须存在 |
| 表格均使用 \small 字号 | WARN | 表格字应与正文有区分 |
| 表格列宽合理分配 | WARN | 文字多的列宽、文字少的列窄 |
| 图/表编号无手写残留 | WARN | caption 中不得有图1表2字样 |
| 公式均有编号 | WARN | 使用 \begin{equation} 而非 \[ \] |
| 页数符合要求 | WARN | 检查正文/附录边界页 |
| 摘要不超过1页 | WARN | 摘要页独立 |
| 无严重 overfull box | WARN | 超过 10pt 的 overfull 需要处理 |
| PDF 未加密 | HARD FAIL | 提交系统无法读取加密 PDF |
| 身份信息在允许位置 | HARD FAIL | 竞赛规则禁止位置无姓名/学校信息 |

**提交前最终确认：**
- [ ] 摘要和结论中的所有数值都能在正文图表中找到对应
- [ ] 参考文献格式统一，≥10条
- [ ] 附录含代码、长推导、AI工具声明
- [ ] 所有图表在正文中有 D-A-C 三段解读
- [ ] 图/表引用编号与编译后编号一致（\
ef{} 正确解析）
- [ ] 所有表格使用 \\small，列宽分配合理
- [ ] PDF 文件大小 < 50MB


## Quick Action Cards (v3.0)

| When user says... | Agent action |
|-------------------|-------------|
| "求解这道题" / "solve this" | Run full pipeline: analyze -> model -> verify -> paper |
| "只做问题1" | pipeline_manager.py auto --stage model_1_build |
| "生成论文" / "write paper" | **MANDATORY**: `build_docx.py draft.md output.docx` (NOT Pandoc) |
| "检查公式渲染" | build_docx.py validate --input paper.docx |
| "重新生成图表" | plot_figures_nature.py --from-results results.json (CUMCM/51MCM: Chinese labels MANDATORY) |
| "优化模型" | model_remediator.py with quality thresholds |
| "修改论文" / "revise paper" | **IN-PLACE EDIT**: Edit existing DOCX with python-docx (NEVER regenerate from MD) |
| "转换LaTeX"/"Word转LaTeX" | `docx_to_latex.py paper.docx` (DOCX → LaTeX PDF camera-ready) |
| "审阅论文" | paper-structure-qa/SKILL.md checklist |
| "验证模型"/"鲁棒性检查" | `verify_solution.py --question Q1 --model-type prediction` |



---

## Gate Contracts (v5.7.0 ? KyrieZhang329-inspired)

?? Gate ??????????? `enter_condition / pass_criteria / fail_fallback`??? Gate ??????????? DIRTY?

| Gate | ?? | ???? | ???? |
|------|------|---------|---------|
| **G1** | PROBLEM_PARSED | ????+??+?????? | ???????? |
| **G2 ?** | METHOD_VALIDATED | ?????? ?30?PoC + ????? | ?????????PoC |
| **G3** | CODE_REVIEWED | ???????????5?????? | ?????? |
| **G4 ?** | RESULTS_FROZEN | frozen_numbers.json?????? | ????????????? |
| **G5** | PAPER_SECTION_READY | ????????????3??? | ?????? |
| **G6 ??** | AUDIT_LAYER_PASSED | 3??????PASS | ??????? |

> ? = ??????????G2?"??????????"?G4?"???bug???????"?
> ?? = ???????????????????

### Gate ???

```
G1 -> G2 -> G3 -> G4 -> G5 -> G6 -> final assembly
                                   ^
                    consistency-auditor -+
                    completeness-auditor -+-- all must PASS
                    quality-auditor      -+
```

### CLI ??

```bash
# ???? Gate ??
python scripts/quality_gate.py contracts

# G2 PoC ?????
python scripts/quality_gate.py g2_poc

# G4 ??????
python scripts/quality_gate.py g4_stale --subquestion Q1

# G6 ??????
python scripts/quality_gate.py g6_audit --workspace-path CUMCM_Workspace

# P1 ??????
python scripts/quality_gate.py propagate --changed-files code/Q1/model.py results/Q1/report.md
```

---

## P1: Change Propagation Rule (v5.7.0)

?? `code/`?`methods/`?`results/`?`planning/` ???????

1. **grep ???** ???????????????????????????
2. **?????? STALE ???**???????????? STALE + ????
3. ?? `frozen_numbers.json` ???????????? ? ?????? STALE

```bash
python scripts/quality_gate.py propagate --changed-files code/Q1/solve.py
```

---

## G2: PoC Hard Gate (v5.7.0)

**??????????"???????"?**

- ????????? ?30 ? PoC ??
- PoC ???????????????????????????"???????"?
- ?? PoC ??? = ????????????

```bash
python scripts/quality_gate.py g2_poc --poc-dir CUMCM_Workspace/methods
python scripts/gate_contracts.py poc
```

---

## G6: Independent Audit Layer (v5.7.0)

**???????????? FAIL ????????????????????**

| ??? | ???? | ???? |
|--------|---------|---------|
| **Consistency** | ???? ? ???? ? frozen_numbers.json ? ??? | `paper/audits/cross_media_consistency_audit.md` |
| **Completeness** | ???????+??+??+??? | `paper/audits/completeness_audit.md` |
| **Quality** | ????????????? | `paper/qa_report.md` |

**????**??????? "?" ???????? PASS?????????????

```bash
python scripts/quality_gate.py g6_audit
python scripts/gate_contracts.py g6
```

---

## Frozen Numbers Protocol (v5.7.0 Enhanced)

??? v5.2 ?????????

- **STALE ????**?`frozen_numbers.py verify` ?????????? `"status": "stale"`
- **??????**?
  1. **??** ? `frozen_numbers.py defrost --reason "..."`
  2. **??** ? ????/?????????
  3. **???** ? `frozen_numbers.py re-freeze --subquestion Q1`
- **??????** `frozen_numbers.json`

```bash
# ????????STALE???
python scripts/frozen_numbers.py status

# ?????????
python scripts/frozen_numbers.py re-freeze --subquestion Q1 --source results/Q1/
```

---

## Environment Ping (v5.7.0)

??? session ???????????? workflow-orchestrator ??????

- `git status --short` ? ????????
- `python --version` ? ?? Python ??
- `python -c "import numpy, pandas, matplotlib"` ? ???????
- ?? `planning/`?`methods/`?`code/`?`results/`?`robustness/`?`paper/` ????


### Formula Rendering (v5.0) ? LaTeX ? OMML Auto-Pipeline

**Write equations in standard LaTeX notation:**
- Display: `$$...$$` on separate lines
- Inline: `$...$` within paragraph text

**The pipeline is automatic**: `build_docx.py` uses `latex2mathml` → `mathml2omml` to convert all equations to native Word OMML. No manual OMML construction needed.

### MANDATORY: Paper Generation (v5.1 IRON RULE)

**ALWAYS use `build_docx.py` for final paper generation. Do NOT use Pandoc, do NOT use manual python-docx scripts.**

```bash
python scripts/build_docx.py draft.md output.docx
```

This single command handles:
1. All `$...$` and `$...---
name: math-modeling-contest
description: >
  Industrial-grade math modeling contest agent for CUMCM (国赛), 51MCM (五一赛),
  and MCM/ICM (美赛). Supports dual-mode operation: Autopilot (AI-driven full
  pipeline) or Manual (human-spec-led with mandatory checkpoints). Use when the
  user needs to solve a math modeling contest problem end-to-end, mentions CUMCM,
  51MCM, MCM, ICM, 数学建模, 国赛, 美赛, or asks to build a mathematical model
  for a competition problem. v2.0 adds deep-research literature search, experiment
  design framework, academic integrity gate, 5-reviewer panel with score >=65,
  model dependency DAG, score trajectory tracking, and writing anti-pattern detection.
metadata:
  version: "5.7.1"
  short-description: Math modeling contest v5.7.1 - G1-G6 gate contracts + PoC hard gate + frozen staleness detection + P1 change propagation + independent 3-layer audit + baseline-first modeling + figure D-A-C rule + abstract template + LaTeX verification + L3+ model derivation depth + result traceability + 9000-char substantive floor
---

# Math Modeling Contest Agent v5.7.1

## Word → LaTeX PDF Pipeline (v5.4) ⭐ NEW

**For polished papers:** Convert a human-polished Word (.docx) to LaTeX PDF for camera-ready submission.

### Pipeline

`
Word draft → Human polish → docx_to_latex.py → LaTeX PDF
`

### Usage

`ash
# Convert DOCX to LaTeX + compile to PDF
python scripts/docx_to_latex.py paper.docx

# Convert without compiling (TeX only)
python scripts/docx_to_latex.py paper.docx --no-compile

# Specify output directory
python scripts/docx_to_latex.py paper.docx --output-dir ./output
`

### What it handles

1. **Chinese text** — ctexart class with proper font setup
2. **Formulas** — inline $...$ and display equation environments with auto-numbering
3. **Subscripts** — _b → $a_{b}$, multi-char ABC_{xyz} → $ABC_{xyz}$
4. **Greek letters** — α β γ δ ε θ λ μ σ φ ω → \alpha \beta \gamma etc.
5. **Tables** — three-line table style with ooktabs
6. **Images** — ![caption](path) → \begin{figure}...\includegraphics
7. **Sections** — 1. Title → \section, 1.1 → \subsection
8. **Footer** — thanks + contact + contest info

### When to use

| Scenario | Tool |
|----------|------
## Word → LaTeX PDF Pipeline (v5.4) ⭐ NEW

**For polished papers:** Convert a human-polished Word (.docx) to LaTeX PDF for camera-ready submission.

### Pipeline

`
Word draft → Human polish → docx_to_latex.py → LaTeX PDF
`

### Usage

`ash
# Convert DOCX to LaTeX + compile to PDF
python scripts/docx_to_latex.py paper.docx

# Convert without compiling (TeX only)
python scripts/docx_to_latex.py paper.docx --no-compile

# Specify output directory
python scripts/docx_to_latex.py paper.docx --output-dir ./output
`

### What it handles

1. **Chinese text** — ctexart class with proper font setup
2. **Formulas** — inline $...$ and display equation environments with auto-numbering
3. **Subscripts** — _b → $a_{b}$, multi-char ABC_{xyz} → $ABC_{xyz}$
4. **Greek letters** — α β γ δ ε θ λ μ σ φ ω → \alpha \beta \gamma etc.
5. **Tables** — three-line table style with ooktabs
6. **Images** — ![caption](path) → \begin{figure}...\includegraphics
7. **Sections** — 1. Title → \section, 1.1 → \subsection
8. **Footer** — thanks + contact + contest info

### When to use

| Scenario | Tool |
|----------|------|
| Quick draft → DOCX | uild_docx.py draft.md output.docx |
| Polished paper → LaTeX PDF | docx_to_latex.py paper.docx |
| LaTeX source → PDF | compile_pdf.py |


|
| Quick draft → DOCX | uild_docx.py draft.md output.docx |
| Polished paper → LaTeX PDF | docx_to_latex.py paper.docx |
| LaTeX source → PDF | compile_pdf.py |


---

## LaTeX 表格排版规范 (v5.7.1)

**所有 LaTeX 表格必须遵守以下规范，逐项检查：**

### 字号规范
| 规则 | 说明 |
|------|------|
| 表格内容用 \small | 比正文小一号，视觉区分明确 |
| 表标题用 \caption{} | 正常字号，加粗（caption 包自动处理） |
| 禁止表格字号与正文相同 | 正文 \normalsize(12pt)，表格 \small(~11pt) |

### 列宽分配规范
| 规则 | 说明 |
|------|------|
| 文字多的列 → 宽 | 如设定依据菜品组合，应占 50-65% 宽度 |
| 文字少的列 → 窄 | 如毛利率单价，只占 8-12% 宽度 |
| 禁止均匀分配 | Pandoc 生成的等宽列必须重新调整 |
| 数值列可用 c 居中 | 纯数字/百分比列用 c 自动宽度 |

**列宽调整公式**（以 longtable 的 p{} 列为例）：
`
p{(\linewidth - N*\tabcolsep) * \real{X.XX}}
`
其中 N = 列数，X.XX 为比例（所有列比例之和应接近 1.00）。

### 跨页表格 (longtable) 规范
| 规则 | 说明 |
|------|------|
| \caption{} 必须在 \endfirsthead 内 | 否则跨页时 label multiply-defined |
| \endhead 前重复表头行 | 每页顶部都显示列名 |
| \endfirsthead 后补 \endhead | 保持结构完整 |

`
{\small\begin{longtable}{@{}...@{}}
\caption{表标题}\label{tab:xxx}\\
\toprule
列1 & 列2 & 列3 \\
\midrule
\endfirsthead           % ← 标题只出现在首页
\toprule
列1 & 列2 & 列3 \\     % ← 后续页重复表头
\midrule
\endhead
\bottomrule
\endlastfoot
... 数据行 ...
\end{longtable}}
`

### 表格常见问题修复

| 问题 | 现象 | 修复方法 |
|------|------|---------|
| 列宽不均 | 百分比列占半页宽，描述列被挤压 | 调整 \real{X.XX} 比例 |
| Pandoc 残留修饰 | >{} 或 \arraybackslash 出现 | post_process_latex() 自动清理 |
| label multiply-defined | 编译警告 | 添加 \endfirsthead |
| 表格无 \small | 表格字与正文一样大 | 用 {\small\begin{longtable}...} 包裹 |

---

## LaTeX 图表编号与交叉引用规范 (v5.7.1)

### 图表编号规范
| 规则 | 说明 |
|------|------|
| 图片用 \label{fig:imgN} | N 为图片序号，LaTeX 自动编号为图1图2 |
| 表格用 \label{tab:xxx} | xxx 为描述性标签，LaTeX 自动编号为表1表2 |
| 公式用 \label{eq:xxx} | xxx 为描述性标签，LaTeX 自动编号为(1)(2) |
| **禁止手动写编号** | \caption 中不得出现图1表2等手写编号 |
| caption 只保留描述文字 | 正确：\caption{菜品销售频次 Top 20} |

### 交叉引用规范
| 规则 | 说明 |
|------|------|
| 文中用 \ref{fig:imgN} | 编译后自动匹配当前图号 |
| 禁止硬编码如图1所示 | 必须用 如图\ref{fig:img1}所示 |
| 表中引用同理 | 如表\ref{tab:costrate}所示 |
| 公式引用 | 式(\ref{eq:profit}) → 编译后显示正确编号 |
| **post_process_latex() 已自动转换** | 文中图N→\ref{fig:imgN} 自动完成 |

### 图片管理规范
| 规则 | 说明 |
|------|------|
| 所有图片放 igures/ 文件夹 | 统一管理，无冗余 |
| 禁止图片散落在根目录 | 只保留 igures/ 一份 |
| 禁止 images/ 重复文件夹 | 删除，统一用 igures/ |
| 编译后清理 | .aux .log .toc .out 删除 |

---

## LaTeX 公式规范 (v5.7.1)

### 公式环境选择
| 规则 | 说明 |
|------|------|
| 需要编号的公式 | \begin{equation}...\end{equation} |
| 不需要编号的 | \begin{equation*}...\end{equation*} |
| 多行对齐 | \begin{aligned} 嵌套在 equation 内 |
| 约束大括号 | \left\{\begin{aligned}...\end{aligned}\right. |
| **禁止 \[...\]** | 无编号，不符合数模论文要求 |

### 模型约束格式规范
优化模型的约束条件必须用大括号格式：
`latex
\begin{equation}
\left\{
\begin{aligned}
& \sum_{i=1}^{N} e_i x_i \geq 0.85 \cdot D \cdot 750  && \text{（热量下限）} \\[4pt]
& \sum_{i=1}^{N} r_i x_i \geq D \cdot 35               && \text{（蛋白质下限）} \\[4pt]
\end{aligned}
\right.
\end{equation}
`

---

## LaTeX 编译后自动修复清单 (v5.7.1)

**post_process_latex() 自动执行以下修复，每次编译前必须检查：**

| # | 修复项 | 说明 |
|---|--------|------|
| 1 | 图/表 caption 去手写编号 | 图1 xxx → xxx |
| 2 | 文中图N→\ref{fig:imgN} | 自动替换 |
| 3 | \[...\]→\begin{equation} | 公式自动编号 |
| 4 | Pandoc >{}/\arraybackslash 清理 | 表格修饰清理 |
| 5 | 孤儿 \end{figure} 清理 | 多余的结束标签删除 |
| 6 | 空 caption \caption{} 清理 | 无内容标题删除 |
| 7 | 	ab:symbols 等跨页表 \endfirsthead | 防止 label multiply-defined |
| 8 | 所有 longtable 加 {\small...} 包裹 | 字号统一 |
| 9 | \headheight 设为 14pt | 消除 fancyhdr 警告 |
| 10 | hidelinks 已默认开启 | 目录无红框 |

## PAPER GENERATION — MANDATORY WORKFLOW (READ FIRST)

**论文操作分两条路径，先判断再执行：修改已有论文 → python-docx 原地编辑；首次生成 → Markdown → build_docx.py。详见上方 PAPER REVISION IRON RULE。**

**When the user says "生成论文" or "solve this problem", you MUST follow these steps IN ORDER:**

### Step 1: Write a complete Markdown draft
- Use `$...$` for display equations, `$...---
name: math-modeling-contest
description: >
  Industrial-grade math modeling contest agent for CUMCM (国赛), 51MCM (五一赛),
  and MCM/ICM (美赛). Supports dual-mode operation: Autopilot (AI-driven full
  pipeline) or Manual (human-spec-led with mandatory checkpoints). Use when the
  user needs to solve a math modeling contest problem end-to-end, mentions CUMCM,
  51MCM, MCM, ICM, 数学建模, 国赛, 美赛, or asks to build a mathematical model
  for a competition problem. v2.0 adds deep-research literature search, experiment
  design framework, academic integrity gate, 5-reviewer panel with score >=65,
  model dependency DAG, score trajectory tracking, and writing anti-pattern detection.
metadata:
  version: "5.7.1"
  short-description: Math modeling contest v5.7.1 - G1-G6 gate contracts + PoC hard gate + frozen staleness detection + P1 change propagation + independent 3-layer audit + baseline-first modeling + figure D-A-C rule + abstract template + LaTeX verification + L3+ model derivation depth + result traceability + 9000-char substantive floor
---

# Math Modeling Contest Agent v5.7.1

### PAPER REVISION — IN-PLACE EDIT (v5.6.1 IRON RULE)

**修改已有论文初稿时，必须在原文档基础上直接编辑，禁止重新生成新文档。**

| 场景 | 正确做法 | 禁止做法 |
|------|---------|---------|
| 修改论文内容/措辞 | 用 python-docx 打开原 DOCX，直接编辑段落 | ❌ 从 Markdown 重新 build_docx.py |
| 增删图表 | 在原 DOCX 中插入/删除图片和表格 | ❌ 重新生成整个文档 |
| 调整格式 | 在原 DOCX 中修改样式/字体/边距 | ❌ 新建文档 |
| 首次生成论文 | uild_docx.py draft.md output.docx ✅ | — |
| 完全重写论文 | 可新建，但必须先确认用户意图 | — |

**为什么必须在原文档上改：**
1. **保留已有内容** —— 重新生成可能丢失人工打磨的措辞、调整过的格式
2. **保留嵌入资源** —— 重新生成会丢失已嵌入的图片（445KB → 67KB）
3. **节省时间** —— 原地编辑比全流程重建快 3-5 倍
4. **降低风险** —— 每次重建引入新的公式渲染、排版风险

**操作规范：**
- 打开原 DOCX → 定位到需修改的段落 → 编辑 → 保存
- 版本命名：首次修改保存为 xxx_v2.docx，后续递增 xxx_v3.docx
- 修改完成后告知用户：改了哪些段落、哪些图表、文件保存位置
- **绝不**在用户说"修改论文"时启动 uild_docx.py 流程


Industrial-grade agent for CUMCM (国赛), 51MCM (五一赛), and MCM/ICM (美赛).
Drives the entire modeling pipeline from problem to paper.




### LaTeX 编译验证清单 (v5.6 —— 集成自 math-modeling-competition-workflow)

**每次 LaTeX 编译后必须逐项检查：**

| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 编译至少两次 | HARD FAIL | 交叉引用需要两次编译才能正确解析 |
| 无 fatal error | HARD FAIL | 任何 ! 开头的 fatal error 必须修复 |
| 无 undefined references | HARD FAIL | 所有 \ref{} 和 \cite{} 必须解析 |
| 无 multiply-defined labels | HARD FAIL | 跨页 longtable 检查 \endfirsthead |
| 无 missing figures | HARD FAIL | 所有 \includegraphics 路径必须存在 |
| 表格均使用 \small 字号 | WARN | 表格字应与正文有区分 |
| 表格列宽合理分配 | WARN | 文字多的列宽、文字少的列窄 |
| 图/表编号无手写残留 | WARN | caption 中不得有图1表2字样 |
| 公式均有编号 | WARN | 使用 \begin{equation} 而非 \[ \] |
| 页数符合要求 | WARN | 检查正文/附录边界页 |
| 摘要不超过1页 | WARN | 摘要页独立 |
| 无严重 overfull box | WARN | 超过 10pt 的 overfull 需要处理 |
| PDF 未加密 | HARD FAIL | 提交系统无法读取加密 PDF |
| 身份信息在允许位置 | HARD FAIL | 竞赛规则禁止位置无姓名/学校信息 |

**提交前最终确认：**
- [ ] 摘要和结论中的所有数值都能在正文图表中找到对应
- [ ] 参考文献格式统一，≥10条
- [ ] 附录含代码、长推导、AI工具声明
- [ ] 所有图表在正文中有 D-A-C 三段解读
- [ ] 图/表引用编号与编译后编号一致（\
ef{} 正确解析）
- [ ] 所有表格使用 \\small，列宽分配合理
- [ ] PDF 文件大小 < 50MB


## Quick Action Cards (v3.0)

| When user says... | Agent action |
|-------------------|-------------|
| "求解这道题" / "solve this" | Run full pipeline: analyze -> model -> verify -> paper |
| "只做问题1" | pipeline_manager.py auto --stage model_1_build |
| "生成论文" / "write paper" | **MANDATORY**: `build_docx.py draft.md output.docx` (NOT Pandoc) |
| "检查公式渲染" | build_docx.py validate --input paper.docx |
| "重新生成图表" | plot_figures_nature.py --from-results results.json (CUMCM/51MCM: Chinese labels MANDATORY) |
| "优化模型" | model_remediator.py with quality thresholds |
| "修改论文" / "revise paper" | **IN-PLACE EDIT**: Edit existing DOCX with python-docx (NEVER regenerate from MD) |
| "转换LaTeX"/"Word转LaTeX" | `docx_to_latex.py paper.docx` (DOCX → LaTeX PDF camera-ready) |
| "审阅论文" | paper-structure-qa/SKILL.md checklist |

### Formula Rendering (v5.0) ? LaTeX ? OMML Auto-Pipeline

**Write equations in standard LaTeX notation:**
- Display: `$$...$$` on separate lines
- Inline: `$...$` within paragraph text

**The pipeline is automatic**: `build_docx.py` uses `latex2mathml` → `mathml2omml` to convert all equations to native Word OMML. No manual OMML construction needed.

### MANDATORY: Paper Generation (v5.1 IRON RULE)

**ALWAYS use `build_docx.py` for final paper generation. Do NOT use Pandoc, do NOT use manual python-docx scripts.**

```bash
python scripts/build_docx.py draft.md output.docx
```

This single command handles:
1. All `$...$` and `$...---
name: math-modeling-contest
description: >
  Industrial-grade math modeling contest agent for CUMCM (国赛), 51MCM (五一赛),
  and MCM/ICM (美赛). Supports dual-mode operation: Autopilot (AI-driven full
  pipeline) or Manual (human-spec-led with mandatory checkpoints). Use when the
  user needs to solve a math modeling contest problem end-to-end, mentions CUMCM,
  51MCM, MCM, ICM, 数学建模, 国赛, 美赛, or asks to build a mathematical model
  for a competition problem. v2.0 adds deep-research literature search, experiment
  design framework, academic integrity gate, 5-reviewer panel with score >=65,
  model dependency DAG, score trajectory tracking, and writing anti-pattern detection.
metadata:
  version: "5.7.1"
  short-description: Math modeling contest v5.7.1 - G1-G6 gate contracts + PoC hard gate + frozen staleness detection + P1 change propagation + independent 3-layer audit + baseline-first modeling + figure D-A-C rule + abstract template + LaTeX verification + L3+ model derivation depth + result traceability + 9000-char substantive floor
---

 for inline
- Use `[FIGURE: filename.png | 图X Title]` for figures
- Table caption: put "**表N 标题**" on the line BEFORE the table body
- Table body: use standard Markdown `| col1 | col2 |` then `|---|---|`
- Hard minimum: **9,000 substantive Chinese characters**. There is no artificial upper/target length.
- Let the final length follow the problem depth, data volume, derivations, experiments, and result interpretation.
- If below the hard minimum, expand with derivation, baseline comparison, robustness, error analysis, and figure/table interpretation only.
- Each sub-problem model chapter MUST have >= 2,000 chars

### Step 2: Generate DOCX with build_docx.py (NO EXCEPTIONS)
```bash
python scripts/build_docx.py draft.md output.docx
```
This ONE command handles:
- All `$...$` → Word native OMML equations (NOT pictures, NOT plain text)
- All `[FIGURE:]` → embedded PNG images with captions
- All markdown tables → CUMCM three-line tables
- Content length check: **< 9,000 chars = HARD FAIL; 9,000+ chars = PASS with no artificial length target**

### Step 3: If HARD FAIL, expand with evidence
- Do NOT bypass with Pandoc, python-docx, or manual scripts
- Expand model chapters with traceable modeling content, not filler.
- Retry `build_docx.py` until it passes

### FORBIDDEN PATHS
- ❌ `pandoc paper.md -o paper.docx` — DO NOT USE
- ❌ Manual `Document()` + `add_paragraph()` — DO NOT USE
- ❌ Any workflow that skips `build_docx.py` content check


### PAPER REVISION — IN-PLACE EDIT (v5.6.1 IRON RULE)

**修改已有论文初稿时，必须在原文档基础上直接编辑，禁止重新生成新文档。**

| 场景 | 正确做法 | 禁止做法 |
|------|---------|---------|
| 修改论文内容/措辞 | 用 python-docx 打开原 DOCX，直接编辑段落 | ❌ 从 Markdown 重新 build_docx.py |
| 增删图表 | 在原 DOCX 中插入/删除图片和表格 | ❌ 重新生成整个文档 |
| 调整格式 | 在原 DOCX 中修改样式/字体/边距 | ❌ 新建文档 |
| 首次生成论文 | uild_docx.py draft.md output.docx ✅ | — |
| 完全重写论文 | 可新建，但必须先确认用户意图 | — |

**为什么必须在原文档上改：**
1. **保留已有内容** —— 重新生成可能丢失人工打磨的措辞、调整过的格式
2. **保留嵌入资源** —— 重新生成会丢失已嵌入的图片（445KB → 67KB）
3. **节省时间** —— 原地编辑比全流程重建快 3-5 倍
4. **降低风险** —— 每次重建引入新的公式渲染、排版风险

**操作规范：**
- 打开原 DOCX → 定位到需修改的段落 → 编辑 → 保存
- 版本命名：首次修改保存为 xxx_v2.docx，后续递增 xxx_v3.docx
- 修改完成后告知用户：改了哪些段落、哪些图表、文件保存位置
- **绝不**在用户说"修改论文"时启动 uild_docx.py 流程


Industrial-grade agent for CUMCM (国赛), 51MCM (五一赛), and MCM/ICM (美赛).
Drives the entire modeling pipeline from problem to paper.




### LaTeX 编译验证清单 (v5.6 —— 集成自 math-modeling-competition-workflow)

**每次 LaTeX 编译后必须逐项检查：**

| 检查项 | 严重性 | 说明 |
|--------|--------|------|
| 编译至少两次 | HARD FAIL | 交叉引用需要两次编译才能正确解析 |
| 无 fatal error | HARD FAIL | 任何 ! 开头的 fatal error 必须修复 |
| 无 undefined references | HARD FAIL | 所有 \ref{} 和 \cite{} 必须解析 |
| 无 multiply-defined labels | HARD FAIL | 跨页 longtable 检查 \endfirsthead |
| 无 missing figures | HARD FAIL | 所有 \includegraphics 路径必须存在 |
| 表格均使用 \small 字号 | WARN | 表格字应与正文有区分 |
| 表格列宽合理分配 | WARN | 文字多的列宽、文字少的列窄 |
| 图/表编号无手写残留 | WARN | caption 中不得有图1表2字样 |
| 公式均有编号 | WARN | 使用 \begin{equation} 而非 \[ \] |
| 页数符合要求 | WARN | 检查正文/附录边界页 |
| 摘要不超过1页 | WARN | 摘要页独立 |
| 无严重 overfull box | WARN | 超过 10pt 的 overfull 需要处理 |
| PDF 未加密 | HARD FAIL | 提交系统无法读取加密 PDF |
| 身份信息在允许位置 | HARD FAIL | 竞赛规则禁止位置无姓名/学校信息 |

**提交前最终确认：**
- [ ] 摘要和结论中的所有数值都能在正文图表中找到对应
- [ ] 参考文献格式统一，≥10条
- [ ] 附录含代码、长推导、AI工具声明
- [ ] 所有图表在正文中有 D-A-C 三段解读
- [ ] 图/表引用编号与编译后编号一致（\
ef{} 正确解析）
- [ ] 所有表格使用 \\small，列宽分配合理
- [ ] PDF 文件大小 < 50MB


## Quick Action Cards (v3.0)

| When user says... | Agent action |
|-------------------|-------------|
| "求解这道题" / "solve this" | Run full pipeline: analyze -> model -> verify -> paper |
| "只做问题1" | pipeline_manager.py auto --stage model_1_build |
| "生成论文" / "write paper" | **MANDATORY**: `build_docx.py draft.md output.docx` (NOT Pandoc) |
| "检查公式渲染" | build_docx.py validate --input paper.docx |
| "重新生成图表" | plot_figures_nature.py --from-results results.json (CUMCM/51MCM: Chinese labels MANDATORY) |
| "优化模型" | model_remediator.py with quality thresholds |
| "修改论文" / "revise paper" | **IN-PLACE EDIT**: Edit existing DOCX with python-docx (NEVER regenerate from MD) |
| "转换LaTeX"/"Word转LaTeX" | `docx_to_latex.py paper.docx` (DOCX → LaTeX PDF camera-ready) |
| "审阅论文" | paper-structure-qa/SKILL.md checklist |

### Formula Rendering (v5.0) ? LaTeX ? OMML Auto-Pipeline

**Write equations in standard LaTeX notation:**
- Display: `$$...$$` on separate lines
- Inline: `$...$` within paragraph text

 → Word native OMML equations (latex2mathml → mathml2omml)
2. All `[FIGURE: file.png | caption]` → embedded images with captions
3. All markdown tables → three-line tables (CUMCM standard)
4. Content length check: < 9,000 substantive chars → **HARD FAIL, DOCX not generated**; 9,000+ chars → PASS
5. Font setup: SimSun body + SimHei headings + Times New Roman English
6. Page setup: A4, 2.54cm/3.17cm margins

**If build_docx.py rejects your paper (HARD FAIL), expand the content until it passes. Do NOT bypass with Pandoc or manual scripts.**

**Examples:**
```markdown
The heat equation:
$$ \frac{\partial T}{\partial t} = \alpha \nabla^2 T + \frac{Q}{\rho c_p} $$

where $\alpha = k/(\rho c_p)$ is the thermal diffusivity.
```

**Dependencies** (install once):
```bash
pip install latex2mathml mathml2omml
```

### Algorithm Selection Flow

**New in v3.1: Physics Model Support** ? For interference, diffraction, wave propagation, heat conduction, and diffusion problems, consult `references/model-formulation-guide.md` Sections 2.7-2.9. These templates enforce derivation chains from physical laws to final formulas.

### Algorithm Selection Flow

Before building models, consult `references/problem-algorithm-map.json`:
1. Match problem keywords to algorithm categories
2. Try `primary` algorithms first
3. Fall back to `alternative` only if primary fails quality thresholds
4. Document selection rationale in model assumptions



## IRON RULE: MODEL FIRST (v3.0)

**The single most common reason for low scores: confusing "model establishment" with "solution process."**

### What counts as MODEL ESTABLISHMENT:
- Declaring model type explicitly: "建立[线性规划/微分方程/Fabry-Perot干涉/...]模型"
- Defining ALL variables: symbol, Chinese name, unit, type
- Writing complete mathematical formulation: objective function, constraints, governing equations
- Stating assumptions with justification
- Deriving key formulas from first principles or citing literature
- Including symbol tables for each model

### What is SOLUTION PROCESS (NOT model establishment):
- Algorithm pseudocode and flowcharts
- Parameter tuning and cross-validation steps
- Code implementation details
- "Step 1: ..., Step 2: ..." descriptions

### Writing Quality Standard (v5.4)

**Paper prose must follow `references/nature-writing-guide.md`:**
- Abstract: Challenge → Method → Key Result → Impact (NOT table of contents)
- Introduction: backward reasoning before forward writing
- Results: observation → comparison → explanation (NOT narrative list)
- Conclusion: contribution + limitation + future (NOT re-abstract)
- Every claim backed by numbers; no "显著/明显/大大"

### The Golden Ratio:
**Model establishment paragraphs : Solution process paragraphs >= 1 : 1**

If your paper has more solution steps than model formulation, you have a problem.

### Content Length Standard (v4.0)

Hard floor: **9,000 substantive characters**. No artificial upper/target length; write as much as the modeling evidence requires.

| Section | Min chars | Reference depth | Notes |
|---------|-----------|-----------------|-------|
| Abstract | 500 | concise dense summary | Bilingual for MCM/ICM |
| Problem Restatement | 800 | enough to restate each task | Background + restated problem |
| Problem Analysis | 2,000 | data exploration + flow diagram | Data exploration, flow diagram |
| Assumptions + Symbols | 500 | assumptions justified, symbols complete | Each assumption justified |
| **Model Building (CORE)** | **6,000** | largest section by substance | Formal math + derivation (MIN 3 eqs/sub-problem) |
| Results + Verification | 1,000 | tables/figures + interpretation | Tables/figures + interpretation |
| Model Evaluation | 800 | sensitivity + robustness | Sensitivity + robustness |
| References + Appendix | 500 | only necessary support material | Code snippets optional |

**Model Building MUST occupy >= 35% of total content. Below 30% = HARD FAIL.**

### ?? Model Building Self-Check (v5.0)

Before writing to DOCX, verify:
1. [ ] Each sub-problem has a **named model type** declared: "??XXX??"
2. [ ] Each model includes: variable table + governing equations + derivation
3. [ ] At least **3 equations per sub-problem** (not counting symbol definitions)
4. [ ] The word "??" appears at least 20 times in the draft (enforces model-first focus)
5. [ ] Solution process (algorithms/implementation) occupies < 50% of model section
6. [ ] Each assumption is numbered and justified in 1-2 sentences

**If any check fails: regenerate the model section before proceeding to DOCX build.**
**If model section < 6000 characters: the content is too thin. Expand derivations.**


### 论文写作结构规范 (v5.6 —— 集成自 math-modeling-competition-workflow)

#### 章节顺序与内容规则

| 章节 | 内容要求 | 禁止放入 |
|------|---------|---------|
| **问题重述** | 每个子问题单独描述，含背景和数据特征 | 不要放分析、不要放方法 |
| **问题分析** | 每个子问题的数据探索、技术难点、解决思路 | 不要放模型公式、不要放数值结果 |
| **模型建立** | 数学原理 + 目标函数 + 约束 + 推导过程 | **严禁**放数值结果、算法伪代码、求解步骤 |
| **模型求解** | 每个模型/子问题一个求解小节，含结果图表 | 不要重复模型公式（引用即可） |
| **灵敏度/鲁棒性** | 参数扰动分析、模型稳定性验证 | 不要只描述不做定量分析 |
| **结论** | 贡献总结 + 局限性 + 未来方向 | 不要写成摘要的复述 |
| **附录** | 代码、长推导、原始数据表、AI工具声明 | 不要用来凑页数 |

**铁律：模型建立章节只放数学原理，不放数值结果。**

#### 图表三段论规则 (Figure/Table D-A-C Rule)

**每张图/表在正文中必须配有三个要素：**

1. **描述 (Description)** —— 图表展示了什么内容
2. **分析 (Analysis)** —— 观察到了什么模式/对比/趋势
3. **结论 (Conclusion)** —— 由此得出什么决策或答案

`
示例（正确）：
图3展示了三种模型在不同噪声水平下的预测误差对比。
可以看出，XGBoost在低噪声场景下误差最低（RMSE=0.12），
但随着噪声增大（σ>0.5），随机森林的鲁棒性明显优于其他模型。
因此，在实际应用中应根据数据质量选择模型：干净数据用XGBoost，噪声数据用随机森林。
`

**缺失任何一环 = WARN，累计3个WARN = HARD FAIL。**

#### 摘要写作模板

推荐使用一个密集段落，按以下顺序组织：

`
针对问题X，考虑[核心难点]，建立[模型类型]模型，采用[算法]求解，得到[关键数值结果]。
针对问题Y，……（同上模式）。
[最后一句：可靠性说明 + 实际意义]
`

**每条摘要句必须包含：问题 → 模型 → 算法 → 结果，四要素缺一不可。**

**好的方法链写法示例：**

> 本文首先以滑动残差偏差校正模型统一两类传感器尺度；随后基于 Hampel 跳变识别和窗口速度平滑，建立受约束三段回归模型识别阶段；再采用滚动中位数插补和共同异常指标完成多源数据质量控制；在此基础上训练分阶段梯度提升模型预测位移；最后以留一变量组合选择和阶段内速度分位数构建四级预警阈值。

#### 无灌水页数扩展策略

要负责任地扩展正文篇幅，应该通过以下方式：
- 增加数学推导和算法表到模型建立章节
- 增加每个子问题的求解叙述和图表解读
- 增加指标定义和验证理由
- 增加灵敏度、稳定性、物理一致性分析
- 增加局限性和扩展场景讨论

**禁止**通过放大附录、重复问题陈述、或添加无支撑的主张来凑页数。

### Quality Gate Integration (v4.0)

Before paper write stage, `quality_gate.py model_formulation` runs automatically:

**HARD FAIL (blocks paper generation):**
- No model type explicitly declared
- No symbol table present
- Missing formal mathematical formulation (equations/governing laws)
- Solution text >> model text (ratio > 1.5:1)
- Content < 9,000 substantive chars (too short for proper exposition)
- Model building section < 30% of total

**FAIL (significant penalty):**
- No physical law citation for physics models
- Parameter values lack source attribution (>=3 params)
- Model assumptions < 3

**WARNING:**
- Content clears 9,000 chars but lacks derivations, robustness, or figure/table interpretation
- Model building 30-35% of total (borderline)
- No formula derivation path for physics models

## Core Philosophy

**Human as Router, AI as Full-Stack Engine.** AI owns the execution (math
derivation, coding, verification, paper writing), humans own judgment (direction,
assumption validation, final approval). The pipeline enforces mandatory
checkpoints so no unverified result enters the paper.

## What Changed in v2.0

| v1.x | v2.0 |
|------|------|
| Basic problem analysis | `literature_deep_search` stage using ARS deep-research (13-agent systematic lit review) |
| No pre-review integrity check | `integrity_gate` stage (7-class blocking checklist before peer review) |
| 3-reviewer panel, pass at 50 | 5-reviewer full panel, pass at 65+ with calibration |
| Implicit model relationships | `dependency_graph` DAG in pipeline state |
| Ad-hoc model building | `experiment_design` framework before model construction |
| No quality tracking | `score_trajectory` across all stages |
| No writing quality check | Writing anti-pattern detection integrated |

## Knowledge Base

This skill ships with a comprehensive reference library to guide model
selection, role execution, and paper writing. The agent MUST consult these
resources during the appropriate pipeline stages.

### Algorithm Library

Detailed algorithm references covering math principles, applicable scenarios,
visualization, key literature, and code implementations. The agent MUST
consult the relevant algorithm file(s) during `model_N_build`.

| File | Algorithms Covered |
|------|-------------------|
| `references/algorithm-library/01-优化算法说明.md` | LP, IP, DP, GA, PSO, SA, ACO, DE, TS, GWO, immune, whale, sparrow, multi-obj, robust |
| `references/algorithm-library/02-预测类算法说明.md` | Grey GM(1,1), interpolation, linear reg, NN, SVM, ARIMA, ES, Prophet, LSTM, XGBoost/LightGBM, spatiotemporal |
| `references/algorithm-library/03-评价类算法说明.md` | AHP, Fuzzy-AHP, entropy weight, TOPSIS, GRA, RSR, CV, subjective weighting, DEA, interval evaluation |
| `references/algorithm-library/04-图论与网络分析算法说明.md` | Shortest path, MST, network flow, critical path, Euler/Hamilton path, matching |
| `references/algorithm-library/05-统计分析与数据处理算法说明.md` | Preprocessing, K-Means/hierarchical/DBSCAN clustering, hypothesis testing, PCA, FA, CCA, NMF |
| `references/algorithm-library/06-综合类算法说明.md` | Monte Carlo, queuing, game theory, cellular automata, Markov chain, differential equation modeling |
| `references/algorithm-library/07-机器学习算法说明.md` | Random Forest, AdaBoost, Isolation Forest |

Quick start: read `references/algorithm-library/README.md` for the rapid index.

**Model Selection Principles (MANDATORY):**

1. Use elementary methods over advanced ones when possible
2. Use simple methods over complex ones when possible
3. Use methods understandable by more people over niche methods
4. Prefer efficiency, accuracy, and simplicity
5. Avoid neural networks unless traditional methods demonstrably fail

| Problem Type | Recommended Models |
|-------------|-------------------|
| Optimization | Programming models, graph-theoretic models |
| Prediction | Time series, regression, grey prediction |
| Evaluation | AHP, entropy weight, TOPSIS |
| Classification | Clustering, discriminant analysis |


### 建模基线优先策略 (v5.6 —— 集成自 math-modeling-competition-workflow)

**建模必须遵循基线优先原则：先简单可解释 → 再加鲁棒预处理 → 最后才上非线性/集成模型。**

| 阶段 | 做什么 | 检查点 |
|------|--------|--------|
| **阶段1: 简单基线** | 线性回归、灰色预测、AHP、LP/IP 等基础模型 | 必须有可解释的结果，建立性能基线 |
| **阶段2: 鲁棒+验证** | 异常值处理、缺失值插补、时间顺序/分组验证 | 验证方法必须尊重问题结构 |
| **阶段3: 进阶模型** | XGBoost、RF、NN 等（仅在前两阶段不足时） | 必须与基线在相同预处理和划分下对比 |

**禁止行为：**
- 禁止不建基线直接上复杂模型——"听起来高级"不是理由
- 禁止在不同预处理/数据划分下对比模型
- 禁止选择复杂模型后不报告基线性能

**常见竞赛建模组件速查：**

| 问题场景 | 基线方法 | 进阶方法 | 升级条件 |
|----------|---------|---------|---------|
| 传感器标定 | 线性/鲁棒回归 | 样条回归、残差偏差校正 | 残差存在系统模式 |
| 变化点识别 | 鲁棒滤波、速度平滑 | 约束分段回归 | 阶段边界模糊 |
| 缺失数据 | 均值/中位数插补 | 多重插补、KNN插补 | 缺失率>10%且非随机 |
| 异常检测 | Hampel滤波、MAD | 同步多变量标记 | 单变量误报率高 |
| 预测 | 线性基线、ARIMA | RF、GBDT、XGBoost | 非线性关系显著 |
| 变量选择 | 逐一剔除比较 | 排列重要性、SHAP | 变量交互复杂 |

**训练纪律：** 固定随机种子 → 保存产物到 
esults/<problem>/ → 指标记入 summary.md。

### Role Guides

Detailed workflows for each role in the modeling team. The agent MUST read
the corresponding guide at the start of each pipeline stage.

| Guide | When to Read | Purpose |
|-------|-------------|---------|
| `references/role-guides/建模手说明.md` | Start of `problem_analysis` | Problem analysis, model selection principles, terminology standards, tool usage (pdf/xlsx/paper_search) |
| `references/role-guides/编程手说明.md` | Start of `experiment_design` | Code implementation workflow, coding standards, visualization requirements |
| `references/role-guides/论文手说明.md` | Start of `content_assembly` | Paper writing workflow, template usage, writing standards |

### Outstanding Thesis Library

Award-winning CUMCM and MCM/ICM papers for reference during model design and
paper writing. Located in `references/outstanding-thesis/`.

| Contest | Path | Coverage |
|---------|------|----------|
| CUMCM (国赛) | `outstanding-thesis/CUMCM/` | RGV scheduling, membership profiling, assembly line optimization, thermal clothing design |
| MCM/ICM (美赛) | `outstanding-thesis/2017MCM ICM/` | Problems A-F, 27 papers total |

**How to use:** Read relevant papers during `problem_analysis` for structural
and methodological inspiration. The agent should identify: (a) paper structure,
(b) model types used, (c) visualization style, (d) how assumptions are justified.

---

## Pipeline Architecture (v2.0)

```
[init]
  → [problem_analysis]         → Checkpoint ①
  → [literature_deep_search]  → (ARS deep-research: systematic lit review)
  → [data_preprocessing]      → Checkpoint ②
  → [experiment_design]       → (design cards + DAG verification)
  → [model_N_build]           → (per sub-problem, respects dependency_graph)
  → [model_N_verify]          → Checkpoint ③ (per sub-problem, MANDATORY)
  → [sensitivity_analysis]    → Checkpoint ④
  → [content_assembly]        → Checkpoint ⑤ (build_docx.py, HARD FAIL if <9,000 substantive chars)
  → [integrity_gate]          → (7-class academic integrity checklist)
  → [paper_review]            → (5-reviewer panel: methodology + statistical + domain + DA + EIC)
  → [docx_render_qa]          → (iterative: render → inspect → fix, repeat until flawless)
  → [structure_qa]            → (check → auto-fix → re-check until IRON RULES pass)
  → [final_deliver]           → [complete]
```

### Stage Details

| Stage | What happens | Est. Duration |
|-------|-------------|---------------|
| `problem_analysis` | Parse contest problem, identify sub-problems, define scope | 5-10 min |
| `literature_deep_search` | Systematic lit review via ARS deep-research: source verification, cross-source synthesis | 10-15 min |
| `data_preprocessing` | Clean, normalize, handle missing data, generate derived variables | 5-10 min |
| `experiment_design` | Fill design cards for each sub-problem; validate dependency DAG | 5 min |
| `model_N_build` | Select algorithm, derive math, implement code, output results | 10-15 min each |
| `model_N_verify` | Run quality_gate.py, self-verify, sensitivity per problem | 5 min each |
| `sensitivity_analysis` | Cross-model sensitivity, robustness checks | 10 min |
| `content_assembly` | Write Markdown draft → build_docx.py → verify 9,000+ substantive chars + OMML formulas | 20-30 min |
| `integrity_gate` | 7-class academic integrity checklist (citations, data, stats, consistency) | 5 min |
| `paper_review` | Independent 5-reviewer panel review | 10-15 min |
| `docx_render_qa` | Open DOCX in Word, verify OMML formulas render, check layout, figures, tables, and Markdown cleanup | 10-15 min |
| `structure_qa` | Structural validation + auto-fix | 2-5 min |
| `final_deliver` | Export final DOCX/PDF | 5 min |

### literature_deep_search — Systematic Literature Review

This stage leverages the ARS `deep-research` skill (13-agent pipeline) for
systematic literature search before model selection:

1. **Socratic research question refinement** — clarify each sub-problem''s research scope
2. **Systematic literature search** — PRISMA-style source collection
3. **Source verification** — validate DOI/title via Semantic Scholar / CrossRef API
4. **Cross-source synthesis** — identify established methods for this problem type
5. **Risk of bias assessment** — flag low-quality sources

Output: `CUMCM_Workspace/memory/literature_review.md` with verified sources and
methodological recommendations per sub-problem.

### experiment_design — Structured Experiment Planning

Before any model is built, each sub-problem gets an experiment design card:

```yaml
model_id: model_1
depends_on: []        # DAG: other model IDs this depends on
candidate_models:     # At least 2 candidates with rationale
validation_method: "cross_validation"
metrics:              # Metric + threshold + interpretation
baseline: "mean"      # Simplest benchmark
fallback_plan:        # What to do if primary model fails
reproducibility:      # seed, env, data version
```

Design cards are written to `CUMCM_Workspace/memory/experiment_design_{N}.md`.

### Model Dependency DAG

Models declare dependencies via `depends_on` in their design cards. The
pipeline respects these: independent models can run in parallel; dependent
models wait for their prerequisites.

Example DAG stored in `pipeline.json`:
```json
{"model_1": [], "model_2": [], "model_3": ["model_2"], "model_4": ["model_1", "model_3"]}
```

### integrity_gate — Academic Integrity Verification

Before the paper goes to peer review, a 7-class blocking checklist runs:

1. **Citation Integrity** — HARD FAIL if references are fabricated or don''t support claims
2. **Data Integrity** — HARD FAIL if data sources untraceable or ranges impossible
3. **Model Correctness** — HARD FAIL if formulas inconsistent or incomplete
4. **Statistical Validity** — HARD FAIL if p=0.000 without justification
5. **Result Consistency** — HARD FAIL if numbers contradict between sections
6. **Logical Completeness** — HARD FAIL if conclusions lack model support
7. **Expression Standards** — HARD FAIL if model type undeclared or no symbol table

PASS requires: 0 HARD FAILs + ≤5 WARNs. See `references/integrity_gate_checklist.md`.

## Modes

### AP Mode (Autopilot — AI-driven)

AI drives end-to-end. After each stage, AI writes a self-review to
`state/review_request.md` and marks the stage `pending_review`.
In Manual checkpoint-pause, AI pauses; human reviews and writes
`[APPROVED]` or `[REWORK]` in `state/human_intervention.md`.

### Manual Mode (Human-spec-led)

Human specifies:
- Which models to use per sub-problem (`state/human_intervention.md` with `[MANUAL_SPEC]`)
- Which algorithms and parameters
- Model verification criteria and thresholds

AI executes exactly as specified, no deviation. Flag mismatches as warnings.

---

## Paper Reviewer Gate — 5-Reviewer Panel (v2.0)

After `integrity_gate` passes, the pipeline pauses at the **reviewer gate**.
The orchestrator spawns 5 independent reviewer agents from the
`academic-paper-reviewer` skill:

1. **methodology_reviewer**: statistical validity, design rigor, reproducibility
2. **statistical_reviewer**: quantitative correctness, model metrics verification
3. **domain_reviewer**: problem-domain relevance, practical applicability
4. **devils_advocate**: core argument challenges, logical fallacies, counter-arguments
5. **eic_agent**: overall quality, originality, completeness, editorial decision

### Pass Criteria (v2.0)

| Criterion | Threshold |
|-----------|-----------|
| CRITICAL issues | 0 (HARD FAIL otherwise) |
| MAJOR issues | ≤ 1 |
| Overall score | ≥ 65/100 |
| Acceptable decisions | Accept, Minor Revision |
| Max review cycles | 3 |

### Calibration (Optional)

Set `calibration_enabled: true` in `references/review_gate_config.json` and
provide a gold set in `references/review_calibration_gold.json` for FNR/FPR
measurement.

### Orchestrator Flow

```
1. Extract paper text from output/paper_C.docx
2. Read reviewer agent definitions from academic-paper-reviewer skill
3. Spawn all 5 reviewer agents in parallel
4. Collect structured verdicts from each
5. Parse for CRITICAL/MAJOR issues and editorial decision
6. Write verdict to state/review_verdict.json
7. PASS → advance to docx_render_qa
8. FAIL → read reports as revision roadmap, rework, re-review (max 3 cycles)
```

---

## Score Trajectory Tracking

Each stage completion records metrics to `pipeline.json` → `score_trajectory`:

```json
{"stage": "model_1_verify", "timestamp": "...", "metrics": {"R²": 0.85}, "passed": true, "reworks": 0}
```

Allows post-mortem analysis: which stages consistently need rework? Where does
quality drop?

---

## Quality Gates

At the end of `model_N_verify` and `content_assembly`, run quality gates:

```bash
# Model verification gates
python scripts/quality_gate.py verify   --stage model_1_verify --report-file REPORT
python scripts/quality_gate.py sanity   --stage model_1_build  --output-file OUTPUT
python scripts/quality_gate.py model_quality --report-text "R²=0.85, MAE=0.07"

# Paper assembly gates (v2.0)
python scripts/quality_gate.py depth    --docx-path output/paper_C.docx
python scripts/quality_gate.py formula  --docx-path output/paper_C.docx
python scripts/quality_gate.py figure_ctx --docx-path output/paper_C.docx

# Integrity gate (v2.0)
python scripts/quality_gate.py integrity --docx-path output/paper_C.docx
```

All gates MUST PASS before advancing to the next stage.

### Model Quality Thresholds

| Metric | Threshold | Gate Level | Category |
|--------|-----------|------------|----------|
| Regression R² | ≥ 0.05 | MIN | model_quality |
| CV R² | NOT < -0.5 | HARD FAIL | model_quality |
| Classification AUC | ≥ 0.70 | MIN | model_quality |
| Classification recall | ≥ 0.20 | MIN | model_quality |

### AUTO-REMEDIATION Triggers

When any HARD FAIL occurs during `model_N_verify`:

1. **R² < 0.05**: Try log/sqrt/Box-Cox transforms, add interaction terms, polynomial features, or switch model.
2. **CV R² < -0.5**: Model has NO predictive power. Report honestly; do NOT fabricate improvements.
3. **AUC < 0.70**: Try class weighting, SMOTE oversampling, or different algorithms.
4. **Section < 3 paragraphs**: Regenerate with required structure.
5. **Figure missing context**: Add interpretation paragraph after figure.

---

## References

| File | Purpose |
|------|---------|
| `references/format-spec-51mcm.md` | 51MCM paper formatting rules |
| `references/model-formulation-guide.md` | Model formulation templates (9 types incl. physics) with mandatory self-check |
| `references/nature-figure-guide.md` | Nature journal figure making guide |
| `references/nature-writing-guide.md` | Paper writing quality standards |
| `references/documents-workflow.md
│   ├── paper-writing-rules.md         (v5.2: +abstract/solving patterns)` | Step-by-step Documents plugin DOCX building guide |
| `references/integrity_gate_checklist.md` | 7-class academic integrity verification checklist (v2.0) |
| `references/experiment_design_framework.md` | Experiment design framework + DAG spec (v2.0) |
| `references/review_gate_config.json` | 5-reviewer panel config + pass criteria (v2.0) |
| `../paper-structure-qa/SKILL.md` | Paper structure QA skill with IRON RULES checklist |
| `../paper-structure-qa/references/checklist.md` | Full quality checklist with defect patterns |
| `../academic-research-suite/SKILL.md` | ARS deep-research + reviewer skill integration (v2.0) |

---

## Quick Start

```bash
# Initialize pipeline
python scripts/pipeline_manager.py init --mode AP --contest CUMCM --problems 3

# Check status
python scripts/pipeline_manager.py status

# Start first stage
python scripts/pipeline_manager.py start-stage problem_analysis

# Request human review at checkpoint
python scripts/pipeline_manager.py request-review --stage problem_analysis --summary "Analysis complete"

# Advance after approval
python scripts/pipeline_manager.py advance problem_analysis
```

---

## Writing Anti-Pattern Detection (v2.0)

During `content_assembly`, the agent MUST avoid these patterns:

```
FAIL: "建立了数学模型如下：..."
  → Must declare model TYPE: "建立多元线性回归模型如下："

FAIL: "Y = -0.4953 + 0.00126W + 0.00946B"
  → Variables undefined. Must state: W=孕周(周), B=BMI(kg/m²)

FAIL: No symbol table
  → Must include table: symbol | meaning | unit | type

FAIL: Model 2 formula missing: only "P85=13.9周"
  → Must derive: P_g = F_g^{-1}(0.85) where F_g is empirical CDF

FAIL: "假设模型合理" — vague assumption
  → Must list specific, falsifiable assumptions

FAIL: AI-typical phrases: "值得注意的是", "此外", "总的来说" (overuse)
  → Vary sentence openers; use specific transitions
```

---

---

## Parallel Work Coordination (v5.2)

When the user asks for multi-agent or parallel work:

- **Zellij panes**: Assign each pane a non-overlapping task and file ownership. Keep one pane responsible for integration and verification. Avoid multiple Codex panes editing the same file.
- **Codex parallelism**: Split into: Problem Analysis + Model Design / Code Implementation / Figures & Tables / Paper Drafting.
- The integration pane validates that numerical claims match code outputs.

See also: `math-modeling-competition-workflow/references/zellij-codex.md` (if installed).

## Contest Isolation (v5.4) — One Contest, One Workspace

**每个赛题拥有独立的 `contests/{name}/` 工作区，彻底隔离数据、代码和输出。**

### 结构

```
contests/
├── APMCM2025_A_农业灌溉/
│   ├── data/          ← 赛题数据放这里
│   ├── src/           ← 模型代码
│   ├── latex/         ← LaTeX 编译
│   ├── output/        ← 论文(DOCX/PDF) 只属于这个赛题
│   └── README.md      ← 赛题说明
├── 光伏电站发电功率日前预测/
└── 51MCM2026_C_边坡预警/
```

### 使用方法

```bash
# 创建新赛题工作区
python scripts/setup_workspace.py --name "APMCM2025_A_农业灌溉"

# 把赛题数据丢进去
cp 赛题数据/* contests/APMCM2025_A_农业灌溉/data/

# 然后在这个工作区里干活，输出不会和其他赛题混在一起
```


### 自动清理 (v5.4)

**每次比赛完成后，自动清理中间产物，只保留最终结果。**

```bash
# 编译后自动删 .aux/.log/.toc（compile_pdf.py 内置）
python scripts/compile_pdf.py --main paper.tex

# Word→PDF 一键转换 + 自动清理中间文件
python scripts/docx_to_latex.py paper.docx --cleanup

# 手动清理某个赛题
python scripts/cleanup_workspace.py --name "APMCM2025_A_农业灌溉"

# 预览模式（不删除，只看会删什么）
python scripts/cleanup_workspace.py --name "APMCM2025_A_农业灌溉" --dry-run

# 清理全部赛题
python scripts/cleanup_workspace.py --all
```

**清理规则：**
- 删：`.aux` `.log` `.toc` `.synctex.gz` 编译残留
- 删：`paper_v2/v3/v5.docx` 中间版本
- 删：`draft*.md` 中间草稿
- 删：空 `memory/` `state/` 目录
- 留：最终论文 (DOCX/PDF)、图片、赛题数据、核心代码

### 关键规则

- **每个赛题开工前，必须先 `setup_workspace.py --name`**
- **赛题数据放到对应 `data/` 下，别到处乱放**
- **论文输出自动进对应 `output/`，不再进全局 `CUMCM_Workspace/output/`**

## File Map

```
math-modeling-contest/
├── SKILL.md                          (this file)
├── assets/                           (SVG icons)
├── agents/openai.yaml                (agent config)
├── templates/                        (DOCX/LaTeX/MD templates)
├── references/
│   ├── algorithm-library/            (7 categories, 50+ algorithms)
│   ├── role-guides/                  (modeler, programmer, writer)
│   ├── outstanding-thesis/           (award-winning papers)
│   ├── model-formulation-guide.md    (10 sections + L3 derivation depth)
│   ├── integrity_gate_checklist.md   (v2.0 + result traceability)
│   ├── experiment_design_framework.md (v2.0)
│   ├── problem-triage.md             (v5.2: 6-dim problem selection)
│   ├── review_gate_config.json       (v2.0)
│   ├── nature-figure-guide.md
│   ├── nature-writing-guide.md       (v5.4: anti-AI writing patterns)
│   ├── robustness-guide.md          (v5.5: sensitivity & verification)       (v5.4: anti-AI writing patterns)
│   ├── nature-writing-guide.md       (v5.4: anti-AI writing patterns)
│   ├── robustness-guide.md          (v5.5: sensitivity & verification)
│   ├── documents-workflow.md
│   ├── paper-writing-rules.md         (v5.2: +abstract/solving patterns)
│   └── format-spec-51mcm.md
├── scripts/
│   ├── pipeline_manager.py           (state machine v2.0)
│   ├── quality_gate.py               (7 gate types + integrity)
│   ├── setup_workspace.py
│   ├── build_docx.py
│   ├── compile_pdf.py
│   ├── docx_to_latex.py        (Word -> LaTeX PDF)
│   ├── verify_solution.py       (v5.5: robustness + depth checks)
│   ├── make_submission.py       (v5.4: submission package)
│   ├── docx_to_latex.py        (NEW: Word → LaTeX PDF)
│   ├── plot_figures_nature.py
│   ├── audit_figures.py
│   ├── model_remediator.py
│   ├── security_check.py
│   ├── draw_image.py
│   └── frozen_numbers.py
└── CUMCM_Workspace/
    ├── state/
    │   ├── pipeline.json             (pipeline state + DAG + score_trajectory)
    │   ├── review_request.md
    │   ├── review_verdict.json
    │   └── human_intervention.md
    └── memory/
        ├── evaluation_log.md
        ├── thought_process.md
        └── literature_review.md      (v2.0)
```

---

## v5.5 Changelog (2026-06-05)

### Integrated from MathModeling-skills
- **verify_solution.py**: Solution verification engine (baseline comparison, sensitivity, error analysis, extreme scenarios, depth checking)
- **robustness-guide.md**: 8-type robustness check framework with model-type-specific requirements
- **G6 Three-Layer Audit**: Consistency -> Completeness -> Quality in quality_gate.py
- **Method selection enforcement**: experiment design card now requires 2-4 candidate comparison

### Pipeline Hardening
- Model depth check: L3 standard enforced (4/6 checks must pass before advancing)
- Robustness reports: per-question `robustness/Qx/qx_robustness_report.md` auto-generated
- Submission package: `make_submission.py` generates ready-to-submit ZIP

## v5.1 Changelog (2026-05-28)

### Critical Bug Fixes
- **build_docx.py**: Fixed broken `latex2mathml` import (`from latex2mathml import converter as l2m` -> `from latex2mathml.converter import convert as l2m_convert`). The old import caused `l2m.convert()` to throw AttributeError on every call, silently failing all formula rendering. 288/289 formulas now convert successfully.
- **build_docx.py**: Added `[FIGURE: file.png | caption]` placeholder handler with automatic image embedding via `add_picture()`.

### New Enforcement
- **build_docx.py**: Added HARD FAIL content length floor before `doc.save()`. Papers with < 9,000 substantive chars are rejected with a clear error message; 9,000+ chars pass without an artificial upper/target length.
- **build_docx.py**: Section word count reporting (total chars, model section chars) printed before save.

### Quality of Life
- **build_docx.py**: Estimated page count shown in output (chars / 900).
- **SKILL.md**: Explicit dependency check note for `latex2mathml.converter.convert` (not `latex2mathml.converter`).



---

## Troubleshooting & Common Issues (v5.6.0)

### Formula Rendering Problems

| Symptom | Cause | Fix |
|---------|-------|-----|
| Raw `$N_s$` text in DOCX tables | build_docx.py crash / encoding issue | Run pre-check: `python scripts/verify_build.py draft.md` |
| `[WARN] OMML inject` in output | latex2mathml XML bug | Usually harmless; 1-2 warnings normal |
| All formulas fail silently | GBK encoding on Windows | Added `sys.stdout.reconfigure(encoding="utf-8")` internally |
| `begin{aligned}` formulas fail | latex2mathml limitation | Auto-converted to `align*` by `_preprocess_latex()` |

### Build Failures

| Symptom | Cause | Fix |
|---------|-------|------|
| `Result: None` with no errors | Content < 9000 chars or missing images | Run `verify_build.py` for detailed report |
| `HARD FAIL: chars < 9000` | Paper too short | Expand evidence-bearing model derivation, robustness, and result-analysis sections |
| No output at all | stdout encoding crash | Ensure `PYTHONIOENCODING=utf-8` or use the built-in fix |

### Pre-Build Checklist

Run before every paper build:
```bash
python scripts/verify_build.py output/draft_paper.md
```

This checks:
1. UTF-8 encoding setup
2. All Python dependencies installed
3. Markdown content length and structure
4. All [FIGURE:] images exist
5. Common LaTeX issues in formulas

### Post-Build Verification

After building, verify formulas rendered correctly:
```bash
python scripts/quality_gate.py table_formula --docx-path output/paper.docx
```

This checks that table cells containing `$...$` were properly converted to OMML.

### Quick Fixes for Specific Formula Issues

- **`aligned` environment**: Automatically converted to `align*`. No manual fix needed.
- **`eqnarray`**: Auto-converted to `align*`. 
- **`cases` environment**: Works with latex2mathml. If failing, check for special characters.
- **Chinese text in formulas**: Use `\text{中文}` syntax. Works correctly.
- **Superscript/subscript in text**: Use Unicode (e.g., `²` for squared) or `$...$` math mode.

---

## v5.6.0 New Scripts

### `scripts/verify_build.py`
Pre-flight checker that validates markdown, dependencies, images, and formula syntax before building. Run this before `build_docx.py` to catch issues early.

```bash
python scripts/verify_build.py draft.md
# Output: PASS/FAIL for each check with specific fix suggestions
```

### `quality_gate.py table_formula`
New quality gate that checks DOCX for unconverted `$...$` formulas in table cells. HARD FAIL if >5% unconverted.

```bash
python scripts/quality_gate.py table_formula --docx-path output/paper.docx
```

### `build_docx.py` Improvements
- Internal `sys.stdout.reconfigure(encoding="utf-8")` -- no more silent GBK crashes on Windows
- `__main__` block with comprehensive error messages showing exact failure cause
- `_preprocess_latex()` auto-fixes aligned/eqnarray before latex2mathml
- `_add_table_cell_text()` renders inline `$...$` as OMML in table cells
- Returns non-zero exit code on failure for CI/CD integration

## v5.2 Changelog (2026-05-29)

### New — Model Building Depth (user priority)
- **model-formulation-guide.md Section 10**: L1-L4 derivation depth standards, 6-step expansion template, worked example, model-type-specific anchors, self-check checklist
- Every model must reach L3 minimum; core models target L4

### New — Workflow Patterns (from math-modeling-competition-workflow)
- **paper-writing-rules.md Section 7**: Abstract pattern with per-problem sentence template
- **paper-writing-rules.md Section 8**: Solving section 5-step pattern with D-A-C rule
- **integrity_gate_checklist.md**: Result traceability iron rule + figure/table D-A-C mandate
- **problem-triage.md** (NEW): 6-dimension problem selection framework with weighted scoring
- **SKILL.md**: Parallel Work Coordination section


## v5.3.3 Changelog (2026-05-31)

### New — Figure Language Rule
- **nature-figure-guide.md**: Added Contest Language Rule section — CUMCM/51MCM figures MUST use Chinese labels, titles, legends, and annotations. English labels on domestic contest figures are FORBIDDEN.
- **SKILL.md**: Quick Action Cards and Paper Generation workflow now explicitly require Chinese figure labels for CUMCM/51MCM.
- **Enforcement**: Before generating any figure, check contest type. Domestic = Chinese-only. International = English-only. No bilingual/mixed-language figures.

## v5.3.2 Changelog (2026-05-31)

### Critical Fix — Table Formula Rendering (re-implemented)
- **Root cause**: `_add_table_cell_text()` function was lost during an earlier backup restore, causing all `$...$` formulas in table cells to appear as raw text (32 cells affected).
- **Re-implemented**: `_add_table_cell_text(cell, text)` splits cell content by `$...$` segments, renders text as runs and equations as OMML via `latex_to_omml()` + `inject_omml()`.
- **Applied to**: Both header row and data rows in `add_three_line_table()`.
- **Verification**: 33 OMML cells, 0 raw `$` in table cells after rebuild.

## v5.3.1 Changelog (2026-05-31)

### Critical Fix — Markdown Artifacts in DOCX
- **Root cause**: `build_docx.py` only handled `#`/`##`/`###` headings. `####` sub-headings and `---` horizontal rules were written as raw text into DOCX, producing 30+ visible markdown characters in the final document.
- **Fixes applied**:
  1. Added `####` heading handler: auto-strips `#### ` prefix, renders as 12pt bold 宋体
  2. Added `---`/`***`/`___` separator handler: silently skips these lines (no output to DOCX)
  3. Added ` ``` ` code fence handler: silently skips code block delimiters
- **Verification**: Fresh build produces 0 markdown artifacts (verified with automated scan)

### New — In-Place DOCX Editing for Revisions
- **PAPER REVISION section**: All paper modifications now use python-docx to edit the DOCX directly
- Preserves embedded images, OMML equations, and existing formatting across revisions
- Markdown regeneration only used for initial generation or complete rewrites
- Added "修改论文" quick action card

### Rationale
- Regenerating from Markdown loses embedded images (3 images become 0, 445KB → 67KB)
- Each regeneration introduces new rendering risks
- In-place editing is faster and safer for text-level revisions

## v5.6.0 Changelog (2026-05-31)

### Critical Bug Fix -- Table Formula Rendering
- **Root cause**: _add_table_cell_text() was added but uild_paper() function got truncated during patching, losing the entire main processing loop. All previous DOCX builds silently returned None.
- **Secondary root cause**: GBK encoding crash on Unicode characters (e.g., ² in L/m²) suppressed all console output, making debugging impossible.
- **Fixes applied**:
  1. Restored full uild_paper() function from backup
  2. Added sys.stdout.reconfigure(encoding='utf-8') for Windows compatibility  
  3. _add_table_cell_text() properly splits $...$ segments and calls latex_to_omml() for each equation
  4. _preprocess_latex() auto-converts ligned->lign* etc. before passing to latex2mathml
- **Verification**: 116 OMML elements (43 in table cells), 0 raw $...$ texts remaining. All table formulas like $N_s$, $L_{main}$, $C_{total}$ render as native Word equations.

### Earlier fixes (retained)


### Critical Bug Fix — Formula Rendering
- **Root cause**: `latex2mathml` cannot parse `\begin{aligned}` with `&` alignment markers — the most common formula pattern in modeling papers (optimization problems, multi-line derivations, etc.). These formulas silently failed and became `[公式: ...]` placeholders.
- **Fix**: Added `_preprocess_latex()` in `build_docx.py` that auto-converts unsupported environments before passing to `latex2mathml`:
  - `\begin{aligned}` / `\end{aligned}` → `\begin{align*}` / `\end{align*}`
  - `\begin{alignedat}{N}` / `\end{alignedat}` → `\begin{align*}` / `\end{align*}`
  - `\begin{eqnarray}` / `\end{eqnarray}` → `\begin{align*}` / `\end{align*}`
- **Formula failure warning**: If >10% of formulas fail conversion, a prominent `⚠ FORMULA WARNING` is now printed with the failure count. Users no longer discover broken formulas only after opening the DOCX.
- All 10 previously-failing formula types (transport optimization, SVM dual, derivation chains, aligned equations) now pass.
### Quality Improvements
- Model building: Step 0 (formalization) through Step 6 (full model summary) enforced
- Result integrity: every number must trace to code or be labeled assumption
- Abstract: standardized per-problem sentence pattern
- Solving: mandatory 5-step structure per sub-problem






## v5.6.0 Changelog (2026-06-05)

### 集成 math-modeling-competition-workflow 优点

#### 新增 —— 建模基线优先策略
- **三阶段建模流程**：简单基线 → 鲁棒预处理+验证 → 非线性/集成进阶
- **常见竞赛建模组件速查表**：传感器标定、变化点识别、缺失数据、异常检测、预测、变量选择
- **禁止行为**：不建基线直接上复杂模型、不公平对比、不报告基线性能

#### 新增 —— 论文写作结构规范
- **章节顺序与内容规则**：问题重述→问题分析→模型建立→模型求解→灵敏度→结论→附录，每章有明确的"必须放"和"禁止放"
- **铁律**：模型建立章节只放数学原理，不放数值结果

#### 新增 —— 图表三段论规则 (D-A-C Rule)
- 每张图/表必须有：描述(Description) → 分析(Analysis) → 结论(Conclusion)
- 缺失任何一环 = WARN，累计3个WARN = HARD FAIL

#### 新增 —— 摘要写作模板
- 每个子问题摘要句：针对问题X，考虑...，建立...模型，采用...算法，得到...结果
- 四要素缺一不可：问题 → 模型 → 算法 → 结果

#### 新增 —— 无灌水页数扩展策略
- 通过数学推导、算法表、灵敏度分析扩展正文
- 禁止通过放大附录、重复陈述凑页数

#### 新增 —— LaTeX 编译验证清单
- 9项编译后必查清单：两次编译、fatal error、undefined refs、missing figures、页数、摘要、overfull、加密、身份信息
- 提交前5项最终确认

## v5.7.1 Changelog (2026-06-06)

### 新增 ── LaTeX 表格排版规范
- 列宽按内容自动分配：文字多的列宽、文字少的列窄
- 所有表格统一使用 \small 字号（比正文小一号）
- 跨页 longtable 的 \caption 必须放在 \endfirsthead 内，防止 label multiply-defined
- Pandoc 残留修饰符（>{}、\arraybackslash）自动清理
- 表标题居中、位于表格上方（position=above）

### 新增 ── LaTeX 图表编号与交叉引用规范
- 图/表 caption 自动去手写编号，LaTeX 自动编号
- 文中图X/表X自动替换为 \ref{fig:imgX}/\ref{tab:xxx}
- 图片统一放在 igures/ 文件夹，删除 images/ 和根目录重复
- 孤儿 \end{figure} 自动清理
- hidelinks 默认开启，目录无红框

### 新增 ── LaTeX 公式规范
- 全部公式使用 \begin{equation} 自动编号（禁止 \[...\]）
- 优化模型约束条件必须用大括号 \left\{\begin{aligned}...\end{aligned}\right. 格式
- 论文假设部分只列假设，去掉论证依据段落

### 增强 ── docx_to_latex.py
- uild_table() 根据内容长度自动平衡列宽
- post_process_latex() 新增10项自动修复链
- preamble 新增 \setlength{\headheight}{14pt} 消除 fancyhdr 警告

### 增强 ── LaTeX 编译验证清单
- 新增表格字号、列宽、跨页标签检查项
- 新增图表编号与交叉引用匹配检查项
- 新增公式编号检查项

## v5.6.1 Changelog (2026-06-05)

### 修复 —— 论文修改流程：强制原地编辑

**问题**：用户说"修改论文"时，skill 经常重新走 Markdown → build_docx.py 流程生成新文档，导致：
1. 浪费时间（全流程 20-30 分钟 vs 直接编辑 2-5 分钟）
2. 丢失人工打磨的措辞和格式
3. 丢失已嵌入的图片（445KB → 67KB）
4. 引入新的公式渲染和排版风险

**修复**：新增 PAPER REVISION — IN-PLACE EDIT IRON RULE 章节，紧贴 FORBIDDEN PATHS，明确规定：
- 修改已有文档 → 必须 python-docx 原地编辑
- 首次生成 → 才用 build_docx.py
- 完全重写 → 必须先确认用户意图
- 版本命名规范：v2 → v3 → v4 递增

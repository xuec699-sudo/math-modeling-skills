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
  version: "5.3.3"
  short-description: Math modeling contest v5.2 - 6-dim problem triage + abstract/solving templates + L3+ model derivation depth + result traceability + 18-22pg standard
---

# Math Modeling Contest Agent v5.2.1

---

## 
### Format Standard (v5.2.2 -- based on 建模竞赛A题_最终论文.docx)

All generated papers MUST follow the reference template at 	emplates/2026建模竞赛A题_最终论文.docx:

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

**When the user asks to generate a paper or solve a problem, you MUST follow these steps IN ORDER:**

### Step 1: Write a complete Markdown draft
- Use double-dollar for display equations, single-dollar for inline math
- Use [FIGURE: filename.png | Figure X Title] for figures (Chinese title for CUMCM/51MCM, English for MCM/ICM)
- Table caption: put "**表N 标题**" on the line BEFORE the table (or [表题] placeholder appears)
- Table body: use standard Markdown | col1 | col2 | then |---|---|
- Target: 15,000-22,000 Chinese characters (18-22 pages)
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
- Content length check: under 15,000 chars = HARD FAIL, no DOCX generated
- Fonts: SimSun body + SimHei headings + Times New Roman English
- Page: A4, 2.54cm/3.17cm margins

### Step 3: If HARD FAIL, expand and retry
- Do NOT bypass with Pandoc, python-docx, or manual scripts
- Expand model chapters until content >= 15,000 chars
- Retry build_docx.py until it passes

### FORBIDDEN PATHS (DO NOT USE)
- pandoc paper.md -o paper.docx
- Manual Document() + add_paragraph()
- Any workflow that skips build_docx.py content check

---

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
  version: "5.3.3"
  short-description: Math modeling contest v5.2 - 6-dim problem triage + abstract/solving templates + L3+ model derivation depth + result traceability + 18-22pg standard
---

# Math Modeling Contest Agent v5.2.1
---

## PAPER GENERATION — MANDATORY WORKFLOW (READ FIRST)

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
  version: "5.3.3"
  short-description: Math modeling contest v5.2 - 6-dim problem triage + abstract/solving templates + L3+ model derivation depth + result traceability + 18-22pg standard
---

# Math Modeling Contest Agent v5.2.1

Industrial-grade agent for CUMCM (国赛), 51MCM (五一赛), and MCM/ICM (美赛).
Drives the entire modeling pipeline from problem to paper.



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
  version: "5.3.3"
  short-description: Math modeling contest v5.2 - 6-dim problem triage + abstract/solving templates + L3+ model derivation depth + result traceability + 18-22pg standard
---

 for inline
- Use `[FIGURE: filename.png | 图X Title]` for figures
- Table caption: put "**表N 标题**" on the line BEFORE the table body
- Table body: use standard Markdown `| col1 | col2 |` then `|---|---|`
- Target: **15,000-22,000 Chinese characters** (18-22 pages)
- Each sub-problem model chapter MUST have >= 2,000 chars

### Step 2: Generate DOCX with build_docx.py (NO EXCEPTIONS)
```bash
python scripts/build_docx.py draft.md output.docx
```
This ONE command handles:
- All `$...$` → Word native OMML equations (NOT pictures, NOT plain text)
- All `[FIGURE:]` → embedded PNG images with captions
- All markdown tables → CUMCM three-line tables
- Content length check: **< 15,000 chars = HARD FAIL, no DOCX generated**

### Step 3: If HARD FAIL, expand and retry
- Do NOT bypass with Pandoc, python-docx, or manual scripts
- Expand model chapters until content >= 15,000 chars
- Retry `build_docx.py` until it passes

### FORBIDDEN PATHS
- ❌ `pandoc paper.md -o paper.docx` — DO NOT USE
- ❌ Manual `Document()` + `add_paragraph()` — DO NOT USE
- ❌ Any workflow that skips `build_docx.py` content check


Industrial-grade agent for CUMCM (国赛), 51MCM (五一赛), and MCM/ICM (美赛).
Drives the entire modeling pipeline from problem to paper.



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
| "审阅论文" | paper-structure-qa/SKILL.md checklist |

### Formula Rendering (v5.0) ? LaTeX ? OMML Auto-Pipeline

**Write equations in standard LaTeX notation:**
- Display: `$$...$$` on separate lines
- Inline: `$...$` within paragraph text

 → Word native OMML equations (latex2mathml → mathml2omml)
2. All `[FIGURE: file.png | caption]` → embedded images with captions
3. All markdown tables → three-line tables (CUMCM standard)
4. Content length check: < 15,000 chars → **HARD FAIL, DOCX not generated**
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

### The Golden Ratio:
**Model establishment paragraphs : Solution process paragraphs >= 1 : 1**

If your paper has more solution steps than model formulation, you have a problem.

### Content Length Standard (v4.0)

Target: **15,000-22,000 characters, 18-22 pages**

| Section | Min chars | Max chars | Target pages | Notes |
|---------|-----------|-----------|-------------|-------|
| Abstract | 500 | 1,000 | 0.8 | Bilingual for MCM/ICM |
| Problem Restatement | 800 | 1,500 | 1.5 | Background + restated problem |
| Problem Analysis | 2,000 | 3,500 | 3.0 | Data exploration, flow diagram |
| Assumptions + Symbols | 500 | 1,000 | 1.0 | Each assumption justified |
| **Model Building (CORE)** | **8,000** | **12,000** | **9.0** | Formal math + derivation (MIN 3 eqs/sub-problem) |
| Results + Verification | 1,000 | 2,500 | 2.0 | Tables/figures + interpretation |
| Model Evaluation | 800 | 2,000 | 1.5 | Sensitivity + robustness |
| References + Appendix | 500 | 1,500 | 1.5 | Code snippets optional |

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

### Quality Gate Integration (v4.0)

Before paper write stage, `quality_gate.py model_formulation` runs automatically:

**HARD FAIL (blocks paper generation):**
- No model type explicitly declared
- No symbol table present
- Missing formal mathematical formulation (equations/governing laws)
- Solution text >> model text (ratio > 1.5:1)
- Content < 12,000 chars (too short for proper exposition)
- Model building section < 30% of total

**FAIL (significant penalty):**
- No physical law citation for physics models
- Parameter values lack source attribution (>=3 params)
- Model assumptions < 3

**WARNING:**
- Content < 15,000 chars (on the short side)
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
  → [content_assembly]        → Checkpoint ⑤ (build_docx.py, HARD FAIL if <15,000 chars)
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
| `content_assembly` | Write Markdown draft → build_docx.py → verify 15,000+ chars + OMML formulas | 20-30 min |
| `integrity_gate` | 7-class academic integrity checklist (citations, data, stats, consistency) | 5 min |
| `paper_review` | Independent 5-reviewer panel review | 10-15 min |
| `docx_render_qa` | Open DOCX in Word, verify OMML formulas render, check page count 18-22 | 10-15 min |
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
│   ├── nature-writing-guide.md
│   ├── documents-workflow.md
│   ├── paper-writing-rules.md         (v5.2: +abstract/solving patterns)
│   └── format-spec-51mcm.md
├── scripts/
│   ├── pipeline_manager.py           (state machine v2.0)
│   ├── quality_gate.py               (7 gate types + integrity)
│   ├── setup_workspace.py
│   ├── build_docx.py
│   ├── compile_pdf.py
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

## v5.1 Changelog (2026-05-28)

### Critical Bug Fixes
- **build_docx.py**: Fixed broken `latex2mathml` import (`from latex2mathml import converter as l2m` -> `from latex2mathml.converter import convert as l2m_convert`). The old import caused `l2m.convert()` to throw AttributeError on every call, silently failing all formula rendering. 288/289 formulas now convert successfully.
- **build_docx.py**: Added `[FIGURE: file.png | caption]` placeholder handler with automatic image embedding via `add_picture()`.

### New Enforcement
- **build_docx.py**: Added HARD FAIL content length check before `doc.save()`. Papers with < 15,000 chars are rejected with a clear error message showing current vs required length. Estimated page count is reported on success.
- **build_docx.py**: Section word count reporting (total chars, model section chars) printed before save.

### Quality of Life
- **build_docx.py**: Estimated page count shown in output (chars / 900).
- **SKILL.md**: Explicit dependency check note for `latex2mathml.converter.convert` (not `latex2mathml.converter`).



---

## Troubleshooting & Common Issues (v5.2.1)

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
| `Result: None` with no errors | Content < 15000 chars or missing images | Run `verify_build.py` for detailed report |
| `HARD FAIL: chars < 15000` | Paper too short | Expand model derivation sections (target: 2000+ chars per sub-problem) |
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

## v5.2.1 New Scripts

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

## v5.2.1 Changelog (2026-05-31)

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





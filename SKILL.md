---
name: math-modeling-contest
description: >
  Industrial-grade math modeling contest agent for CUMCM, 51MCM, and MCM/ICM.
  Use when the user needs to solve, analyze, write, revise, or audit a math
  modeling contest problem end-to-end, including 数学建模, 国赛, 五一赛, 美赛,
  CUMCM, 51MCM, MCM, and ICM problems. Supports Manual checkpoints and Autopilot
  execution, model design, reproducible code, figure generation, paper writing,
  DOCX/PDF output, and revision workflows.
metadata:
  version: "5.8.0"
  short-description: Math modeling contest pipeline with G1-G6 gates, reproducible modeling, Nature-style figures, 9000-character content floor, and clean DOCX generation
---

# Math Modeling Contest Agent

Use this skill as a contest-solving workflow, not as a generic writing prompt. The agent must keep claims, numbers, code, figures, and paper text traceable to upstream artifacts.

## First Decision

Before doing any work, decide which route applies.

| Route | Use when | Main output |
|---|---|---|
| New solution | User provides a contest problem and wants solving/writing | parsed problem, models, code, figures, Markdown, DOCX |
| Existing DOCX revision | User provides a draft paper and asks to revise it | edited DOCX with change summary |
| Audit only | User asks for review/check/score | findings, risks, required fixes |
| Partial task | User asks for one subproblem, data check, figure, or method | scoped artifact only |

Manual mode is the default for serious contest work. Autopilot is allowed only when the user explicitly asks for full automatic execution.

## One-Sentence Startup Prompt

When a user asks how to invoke the skill, suggest:

```text
Please use the math-modeling-contest skill to solve my uploaded contest problem in Manual checkpoint mode. First read the problem and attachments, split all subproblems, inspect the data, propose 2-3 candidate models for each subproblem, build the dependency DAG, and wait for my confirmation before writing code or the paper.
```

For Chinese users, suggest:

```text
请使用 math-modeling-contest skill 以 Manual checkpoint 模式处理我上传的数学建模赛题。请先读取题目和附件，拆解每一问，检查数据，给每一问提出 2-3 个候选模型，建立问题依赖 DAG，并在我确认路线后再写代码和论文。
```

## Canonical Workflow

Follow these gates in order for a new contest solution. Do not write the paper before verified results exist.

1. G1 Problem Parsed
   - Identify contest type, language, deliverables, uploaded files, and deadlines.
   - Split each subproblem into inputs, outputs, constraints, objectives, metrics, and dependencies.
   - Produce a question dependency DAG. Mark which tasks can run in parallel.

2. G2 Method Validated
   - For each subproblem, propose at least two candidate methods.
   - Compare assumptions, data needs, strengths, weaknesses, and failure modes.
   - Run a minimal PoC or baseline before selecting a complex model.

3. G3 Code Reviewed
   - Use reproducible scripts with explicit input/output paths and fixed seeds where relevant.
   - Save intermediate artifacts: cleaned data, parameters, run logs, result tables, and figure sources.
   - Never invent values. Every reported number must trace back to code, data, or a stated derivation.

4. G4 Results Frozen
   - Freeze final numbers, tables, and figures before paper writing.
   - If code, data, or parameters change, mark downstream text/figures stale and refreeze results.
   - Use `scripts/frozen_numbers.py` when helpful.

5. G5 Paper Section Ready
   - Write from artifacts, not memory.
   - Use Markdown as the source draft for new papers.
   - Every model chapter must include variables, assumptions, formulas, solving steps, results, and interpretation.
   - Every important result should include at least three of: baseline comparison, robustness/sensitivity, uncertainty/error analysis, domain meaning, and cross-subproblem consistency.

6. G6 Audit Layer Passed
   - Check data provenance, formula consistency, statistical validity, citations, unsupported claims, figure/table references, and DOCX rendering.
   - Use the review/audit scripts when available.
   - Deliver only after the audit issues are fixed or explicitly disclosed.

## Content Length Rule

The total paper has a hard floor of 9,000 substantive Chinese characters for Chinese contests. There is no artificial upper limit and no fixed target length.

If the draft is below the floor, expand only evidence-bearing content:

- derivations and variable definitions
- baseline comparisons
- robustness and sensitivity analysis
- uncertainty or error analysis
- data preprocessing details
- figure/table D-A-C interpretation
- limitations grounded in actual results

Never pad with generic background, repeated problem statements, empty significance claims, or unsupported prose.

## Paper Generation

For a new paper:

1. Build a complete Markdown draft.
2. Use display math with `$$...$$` and inline math with `$...$`.
3. Use figure placeholders such as `[FIGURE: fig1.png | Figure 1 Title]`.
4. Put table captions immediately before Markdown tables.
5. Generate DOCX with:

```bash
python scripts/build_docx.py draft.md output.docx
```

Do not use Pandoc as the primary DOCX route. `scripts/build_docx.py` is responsible for:

- native editable Word equations where supported
- CUMCM-style tables
- figure insertion and captions
- SimSun/SimHei/Times New Roman formatting
- Markdown cleanup for stray `*`, `_`, links, bullets, blockquotes, and inline code markers
- hard content-floor validation

For an existing DOCX revision:

1. Inspect the current paper structure.
2. Use `python-docx` or `scripts/edit_inplace.py` to edit in place.
3. Save a new version instead of overwriting the user's original file.
4. Report what changed and where.

## Figure Rules

Borrow the core logic from `nature-figure`: decide the communication goal before plotting.

For every figure:

- Define the claim the figure supports.
- Choose the simplest chart that makes the claim testable.
- Use readable labels, units, legends, and captions.
- Prefer multi-panel figures only when panels answer connected questions.
- Use Chinese labels for CUMCM/51MCM and English labels for MCM/ICM.
- Save source data and plotting code with the output image.
- Explain each figure using D-A-C: describe what is shown, analyze the pattern, conclude what it means for the subproblem.

Useful scripts:

- `scripts/plot_figures_nature.py`
- `scripts/draw_image.py`
- `scripts/audit_figures.py`
- `scripts/gen_chinese_figs.py`

## Modeling Standards

Always prefer a baseline-first modeling path:

1. Establish a simple baseline.
2. Add the selected main model.
3. Compare the main model against the baseline.
4. Add robustness or sensitivity checks.
5. State where the model fails.

For each model, include:

- assumptions and their impact
- variables with units
- objective function or core equation
- constraints or feasible region
- solution method
- parameter sources
- computational procedure
- result interpretation

Read `references/model-formulation-guide.md` for deeper formulation guidance and `references/robustness-guide.md` for robustness checks.

## Integrity Rules

Block delivery if any of these occur:

- fabricated data, references, experiments, or parameter values
- paper numbers not traceable to code/data/derivation
- unsupported performance claims
- stale results after code or data changes
- missing explanation for major assumptions
- figure/table captions that do not match the actual artifact
- equations that are inconsistent with code or text

Use `references/integrity_gate_checklist.md` and `references/qa-checklist.md` for detailed audits.

## Scripts

Use bundled scripts instead of rewriting fragile utilities.

| Need | Preferred script |
|---|---|
| Pipeline orchestration | `scripts/pipeline_manager.py` |
| Gate contracts | `scripts/gate_contracts.py` |
| DOCX generation | `scripts/build_docx.py` |
| DOCX revision | `scripts/edit_inplace.py` |
| Word to LaTeX/PDF | `scripts/docx_to_latex.py`, `scripts/compile_pdf.py` |
| Quality gate | `scripts/quality_gate.py` |
| Paper review | `scripts/review_paper.py`, `scripts/rereview.py` |
| Frozen result tracking | `scripts/frozen_numbers.py` |
| Figure audit | `scripts/audit_figures.py` |
| Data check | `scripts/check_data.py` |
| Final verification | `scripts/final_vfy.py`, `scripts/verify_build.py` |

Read a script before modifying it. Keep edits scoped and verify with a small run whenever possible.

## References To Load On Demand

Load only the reference needed for the current step.

| Step | Reference |
|---|---|
| Problem triage | `references/problem-triage.md`, `references/problem-taxonomy.md` |
| Algorithm choice | `references/problem-algorithm-map.json`, `references/algorithm-library/` |
| Model derivation | `references/model-formulation-guide.md` |
| Experiment design | `references/experiment_design_framework.md` |
| Writing | `references/paper-writing-rules.md`, `references/nature-writing-guide.md` |
| Figures | `references/nature-figure-guide.md` |
| Robustness | `references/robustness-guide.md` |
| Integrity audit | `references/integrity_gate_checklist.md`, `references/qa-checklist.md` |
| 51MCM formatting | `references/format-spec-51mcm.md` |

## Output Style

For Manual mode, after each gate provide:

- `status`: pass, needs_user_decision, needs_fix, or blocked
- `artifacts`: files or results created
- `risks`: unresolved issues
- `next`: the next concrete action

For Autopilot mode, continue working without asking for confirmation unless a blocking ambiguity, missing file, or integrity issue appears.

## Maintenance Rules

Keep this `SKILL.md` concise. Put long examples, contest-specific templates, and detailed rubrics in `references/`. Avoid duplicated frontmatter, repeated workflow blocks, historical changelogs, and garbled text in this file.

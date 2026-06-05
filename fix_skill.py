with open("SKILL.md", "r", encoding="utf-8") as f:
    content = f.read()

troubleshooting = """

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
- **Chinese text in formulas**: Use `\\text{中文}` syntax. Works correctly.
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
"""

# Insert before the v5.2 changelog
old = "## v5.2 Changelog"
content = content.replace(old, troubleshooting + "\n" + old)

with open("SKILL.md", "w", encoding="utf-8") as f:
    f.write(content)
print("SKILL.md updated with troubleshooting + new features docs")

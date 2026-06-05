# Nature-Figure Making Guide for Math Modeling Papers

Integrated from `nature-figure` skill, adapted for CUMCM/MCM contest papers.
Produces publication-quality figures with Nature journal semantic palette,
correct CJK font handling, and built-in data integrity checks.

## Quick Start

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# MANDATORY: SimHei first for CJK, Arial fallback for Latin (FIXED from original nature-figure)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial', 'DejaVu Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['axes.unicode_minus'] = False

# Nature style
plt.rcParams.update({
    'axes.spines.right': False,
    'axes.spines.top': False,
    'legend.frameon': False,
    'axes.linewidth': 0.8,
})
```

## Figure Contract (Establish Before Plotting)

```text
Core conclusion: [one sentence the figure must defend]
Figure archetype: quantitative grid | schematic-led composite | image plate | asymmetric
Target journal/output: CUMCM/MCM paper
Backend: Python (matplotlib)
Final size: [figsize tuple]
Panel map:
  a: [what each panel shows]
  b:
Evidence hierarchy:
  hero evidence:
  validation evidence:
  controls/robustness:
Statistics needed:
Source data needed:
```

## Nature Semantic Palette

```python
PALETTE = {
    "blue_main":      "#0F4D92",  # hero/proposed method
    "blue_secondary": "#3775BA",  # variants
    "green_3":        "#8BCF8B",  # improvement deltas
    "red_strong":     "#B64342",  # bottleneck/warning
    "neutral_light":  "#CFCECE",  # baseline
    "neutral_mid":    "#767676",
    "neutral_dark":   "#4D4D4D",
    "neutral_black":  "#272727",  # text
    "teal":           "#42949E",
    "violet":         "#9A4D8E",
}
```

Semantic rules:
- blue = proposed/optimal solution
- neutral = baseline/comparison
- red = bottleneck/critical
- green = improvement delta (use sparingly)

## Critical FIX: Font Configuration

**DO NOT** use `['Arial', 'SimHei', ...]`. This causes every CJK character to
fail on Arial and emit warnings (hundreds per figure).

**ALWAYS** put SimHei first: `['SimHei', 'Arial', 'DejaVu Sans']`.
SimHei handles CJK natively and has acceptable Latin glyphs; Arial catches
any missing Latin characters.

## Critical FIX: Data Field Name Mismatches

JSON result files may use different field names than expected:

| Expected | Common Actual | Fix |
|----------|--------------|-----|
| `makespan` | `total_duration_seconds` | Read `data.get('makespan', data.get('total_duration_seconds', 0))` |
| `utilization` | NOT PRESENT (must compute) | Compute from schedule: sum(duration) / (device_count * makespan) |

### Utilization Computation Function

```python
def compute_utilization(schedule):
    """Compute utilization from schedule if no utilization key in JSON."""
    device_times = {}
    for r in schedule:
        dtype = r.get('device_type', r.get('equipment_type', 'Unknown'))
        device_times[dtype] = device_times.get(dtype, 0) + r['duration_seconds']
    total_makespan = max(r['start_seconds'] + r['duration_seconds'] for r in schedule)
    utilization = {}
    for dtype, total_time in device_times.items():
        devices_of_type = len(set(r['device_id'] for r in schedule 
                                  if r.get('device_type','') == dtype))
        if devices_of_type > 0 and total_makespan > 0:
            utilization[dtype] = total_time / (devices_of_type * total_makespan)
    return utilization
```

## Common Pitfalls & Fixes

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Chinese shows as boxes | Arial listed before SimHei | Put SimHei first in font.sans-serif |
| Figure is blank (no bars/lines) | JSON field name mismatch | Use .get() with fallback keys |
| Utilization chart empty | No `utilization` key in JSON | Compute from schedule data |
| Gantt labels unreadable | Too many devices | Cap at top_n=25, shorten labels |
| CJK warning flood | Arial tried first for all chars | Always SimHei first |

## Self-Audit Script

Run `scripts/audit_figures.py` to check:
1. Font availability (SimHei, Arial, DejaVu Sans)
2. Data integrity (all JSON fields present)
3. Each figure's data availability
4. Font rendering test panel

Usage:
```bash
python scripts/audit_figures.py
```

## Contest Language Rule for Figures (v5.3.2)

**IRON RULE: Figure labels, titles, legends, and annotations MUST match the contest language.**

| Contest | Language | Figure labels | Axis titles | Legend | Annotations |
|---------|----------|:---:|:---:|:---:|:---:|
| CUMCM (国赛) | 中文 | ✅ 中文 | ✅ 中文 | ✅ 中文 | ✅ 中文 |
| 51MCM (五一赛) | 中文 | ✅ 中文 | ✅ 中文 | ✅ 中文 | ✅ 中文 |
| APMCM (亚太赛) | English | English | English | English | English |
| MCM/ICM (美赛) | English | English | English | English | English |

**Forbidden:**
- ❌ English labels on CUMCM/51MCM figures — will confuse Chinese judges
- ❌ Bilingual labels (中/英混排) — pick ONE language
- ❌ Mixed-language legends (e.g. English legend + Chinese title)

**Enforcement:**
- Before generating any figure, check the contest type
- If contest is CUMCM or 51MCM: ALL text elements MUST be in Chinese
- If contest is MCM/ICM or APMCM: ALL text elements MUST be in English
- Do NOT default to English just because matplotlib or the nature-figure palette is English-oriented

**Quick check before saving:**
```python
# CUMCM/51MCM figures
ax.set_xlabel('时间 (天)')          # NOT 'Time (days)'
ax.set_ylabel('土壤湿度')            # NOT 'Soil Moisture'
ax.set_title('图1 土壤湿度变化趋势')  # NOT 'Fig 1 Soil Moisture Trend'
ax.legend(['随机森林', '梯度提升'])   # NOT ['Random Forest', 'Gradient Boosting']
```

## Export Formats

- **Primary**: SVG (editable text, `svg.fonttype='none'`)
- **Secondary**: PNG at 300 DPI (for DOCX insertion)
- **Never**: PNG-only when text may need adjustment

## Figure Archetype Selection

| Archetype | Use when | Hero panel |
|-----------|---------|-----------|
| `quantitative grid` | Numerical comparison | Dominant summary metric |
| `schematic-led composite` | Workflow/mechanism first | Left/top schematic (35-60%) |
| `image plate + quant` | Images lead evidence | Representative image + scale bar |
| `asymmetric mixed-modality` | Mixed chart types | One panel spans rows/cols |

## Layout Rules

- Never use equal-sized panels when evidence is not equally important
- Keep one palette family per figure
- Prefer direct labels over legends when possible
- No grid lines by default
- Only left + bottom spines
- Frameless legends (`legend.frameon = False`)
- `tight_layout(pad=1.5)` before every save
- Always `plt.close(fig)` after save

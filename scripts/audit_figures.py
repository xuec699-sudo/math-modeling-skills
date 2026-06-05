# -*- coding: utf-8 -*-
"""
Figure Self-Audit Script
Checks font availability, data integrity, renders test panels, reports issues.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json, os, sys
from pathlib import Path
import numpy as np

# Change to project root
os.chdir(r"D:\C盘文档\New project")

print("=" * 65)
print("  FIGURE SELF-AUDIT: Multi-Process Scheduling Paper")
print("=" * 65)

# ============================================================
# STEP 1: Font Diagnosis
# ============================================================
print("\n[1/5] Font availability check")

available = sorted(set(f.name for f in fm.fontManager.ttflist))

fonts_needed = {
    'SimHei': 'Chinese titles/body',
    'Microsoft YaHei': 'Chinese fallback',
    'Arial': 'Latin text',
    'DejaVu Sans': 'Latin fallback',
}

for name, role in fonts_needed.items():
    status = "OK" if name in available else "MISSING!"
    print(f"  {name:25s} ({role:20s}): {status}")

# ============================================================
# STEP 2: Font rendering test panel
# ============================================================
print("\n[2/5] Chinese text rendering test")

# Try different font configurations
configs = [
    ("SimHei only", {'font.family': 'sans-serif', 'font.sans-serif': ['SimHei']}),
    ("SimHei first, Arial fallback", {'font.family': 'sans-serif', 'font.sans-serif': ['SimHei', 'Arial']}),
    ("Microsoft YaHei first", {'font.family': 'sans-serif', 'font.sans-serif': ['Microsoft YaHei', 'Arial']}),
]

OUT = Path("CUMCM_Workspace/latex/images")
OUT.mkdir(parents=True, exist_ok=True)

best_config = None
best_score = 0

fig, axes = plt.subplots(1, 3, figsize=(18, 4))
test_texts = ['图1 各车间工序流程图', '设备利用率 (%)', 'C车间 C3-C5循环次数', '12345.6h 万元']

for idx, (name, rc) in enumerate(configs):
    plt.rcParams.update(rc)
    plt.rcParams['axes.unicode_minus'] = False
    
    ax = axes[idx]
    for i, txt in enumerate(test_texts):
        ax.text(0.5, 0.85 - i*0.2, txt, transform=ax.transAxes,
                ha='center', fontsize=14, fontweight='bold')
    ax.set_title(f'Config: {name}', fontsize=12, fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    print(f"  Tested: {name}")

fig.suptitle('Font Rendering Diagnostic', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT / '_audit_font_test.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"  -> Saved: {OUT / '_audit_font_test.png'}")

# ============================================================
# STEP 3: Data integrity check
# ============================================================
print("\n[3/5] Data integrity check")

data_issues = []
for q in [1, 2, 3, 4]:
    f = Path("CUMCM_Workspace/output") / f"q{q}_result.json"
    if not f.exists():
        data_issues.append(f"Q{q}: result file missing")
        print(f"  Q{q}: MISSING result file!")
        continue
    
    with open(f, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    
    keys = list(data.keys())
    has_schedule = 'schedule' in data and len(data['schedule']) > 0
    has_makespan = 'makespan' in data
    has_utilization = 'utilization' in data
    
    print(f"  Q{q}: keys={keys}, schedule={has_schedule} ({len(data.get('schedule',[]))} entries), makespan={has_makespan}, utilization={has_utilization}")
    
    if not has_schedule:
        data_issues.append(f"Q{q}: empty schedule")
    if has_schedule:
        # Check schedule entries have required fields
        for r in data['schedule'][:3]:
            missing = [k for k in ['device_id','device_type','start_seconds','duration_seconds'] if k not in r]
            if missing:
                data_issues.append(f"Q{q}: schedule entries missing fields: {missing}")

if data_issues:
    print(f"\n  DATA ISSUES FOUND ({len(data_issues)}):")
    for issue in data_issues:
        print(f"    - {issue}")
else:
    print("  All data files OK")

# ============================================================
# STEP 4: Figure-by-figure simulated render check
# ============================================================
print("\n[4/5] Figure data availability per panel")

# Best font config: SimHei first, Arial fallback
best_rc = {'font.family': 'sans-serif', 'font.sans-serif': ['SimHei', 'Arial']}
plt.rcParams.update(best_rc)
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['legend.frameon'] = False

# Load all results
results = {}
for q in [1,2,3,4]:
    f = Path("CUMCM_Workspace/output") / f"q{q}_result.json"
    if f.exists():
        with open(f, 'r', encoding='utf-8') as fp:
            results[q] = json.load(fp)

# Check each figure's data requirements
checks = []

# Fig 1: Workshop flow - no data dependency
checks.append(("Fig 1 (Flow)", True, "Static schematic"))

# Fig 2-5: Gantt charts
for q in [1,2,3,4]:
    ok = q in results and len(results[q].get('schedule', [])) > 0
    checks.append((f"Fig {q+1} (Q{q} Gantt)", ok, 
                   f"{len(results[q].get('schedule',[]))} entries" if ok else "NO DATA"))

# Fig 6: Utilization
ok6 = (2 in results and 'utilization' in results[2]) or (3 in results and 'utilization' in results[3])
checks.append(("Fig 6 (Utilization)", ok6, "Q2+Q3 utilization data" if ok6 else "NO DATA"))

# Fig 7: Makespan comparison
ok7 = any(q in results and 'makespan' in results[q] for q in [1,2,3,4])
vals = {q: results[q].get('makespan', '?') for q in [1,2,3,4] if q in results}
checks.append(("Fig 7 (Makespan)", ok7, str(vals)))

# Fig 8: Sensitivity - computed, no data dependency
checks.append(("Fig 8 (Sensitivity)", True, "Computed from base values"))

# Figs 9-10: Computed from hardcoded + result data
checks.append(("Fig 9 (Bottleneck)", True, "Hardcoded config + Q4 data"))
checks.append(("Fig 10 (Ranking)", True, "Hardcoded workshop times"))

for name, ok, detail in checks:
    status = "OK" if ok else "BLANK!"
    print(f"  {name:25s}: {status:8s} | {detail}")

# ============================================================
# STEP 5: Final recommendations
# ============================================================
print("\n[5/5] Recommendations")

issues = []
for name, ok, detail in checks:
    if not ok:
        issues.append(f"{name}: {detail}")

if issues:
    print(f"  {len(issues)} figure(s) will render BLANK:")
    for i in issues:
        print(f"    - {i}")
    print("\n  SUGGESTED FIX: Re-run the solver scripts to regenerate result JSON files.")
else:
    print("  All figures have valid data.")

print(f"\n  RECOMMENDED FONT CONFIG:")
print(f"    rcParams = {{'font.sans-serif': ['SimHei', 'Arial']}}")
print(f"    rcParams['axes.unicode_minus'] = False")
print(f"    # This puts SimHei first for CJK, Arial fallback for Latin")

print("\n" + "=" * 65)
print("  AUDIT COMPLETE")
print(f"  Diagnostic image: {OUT / '_audit_font_test.png'}")
print("=" * 65)
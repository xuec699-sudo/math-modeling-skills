# -*- coding: utf-8 -*-
"""Generate Chinese-labeled figures for CUMCM paper"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Font: SimHei first for Chinese
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({
    'axes.spines.right': False, 'axes.spines.top': False,
    'legend.frameon': False, 'axes.linewidth': 0.8,
    'figure.dpi': 300, 'savefig.dpi': 300,
    'font.size': 9, 'axes.titlesize': 11, 'axes.labelsize': 9,
    'legend.fontsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
    'figure.facecolor': 'white', 'savefig.facecolor': 'white',
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.12,
})

out_dir = Path(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\latex\images")

# ============================================================
# Fig 1: Farm layout with crops and sprinkler grid
# ============================================================
fig, ax = plt.subplots(figsize=(6, 6))

# Farm boundary
ax.plot([0, 100, 100, 0, 0], [0, 0, 100, 100, 0], 'k-', linewidth=2)

# Crops
ax.fill_between([0, 100], 50, 100, color='#E8D4B8', alpha=0.6)  # sorghum
ax.fill_between([0, 100], 20, 50, color='#C8E6C9', alpha=0.6)   # corn
ax.fill_between([0, 100], 0, 20, color='#BBDEFB', alpha=0.6)    # soybean

# River
ax.fill_between([-5, 0], -5, 105, color='#64B5F6', alpha=0.5)
ax.text(-3, 50, '河流', rotation=90, va='center', ha='center', fontsize=10, color='#1565C0')

# Sprinklers
cols = [25, 50, 75]
rows = [7.5 + i*15 for i in range(7)]
for cx in cols:
    for cy in rows:
        circle = plt.Circle((cx, cy), 15, fill=False, color='#E53935', linewidth=0.8, linestyle='--', alpha=0.6)
        ax.add_patch(circle)
        ax.plot(cx, cy, 'o', color='#C62828', markersize=4)

# Labels
ax.text(50, 75, '高粱 (0.5公顷)', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(50, 35, '玉米 (0.3公顷)', ha='center', va='center', fontsize=10, fontweight='bold')
ax.text(50, 10, '大豆 (0.2公顷)', ha='center', va='center', fontsize=10, fontweight='bold')

ax.set_xlim(-8, 108)
ax.set_ylim(-5, 105)
ax.set_xlabel('x (m)', fontsize=9)
ax.set_ylabel('y (m)', fontsize=9)
ax.set_title('图1 农场作物分布与喷头网格布设示意图', fontsize=11, fontweight='bold')
ax.set_aspect('equal')
fig.tight_layout(pad=1.0)
fig.savefig(out_dir / 'fig1_farm_layout.png', dpi=300)
plt.close(fig)
print("[OK] fig1_farm_layout.png")

# ============================================================
# Fig 2: Pipe topology with sprinkler coverage
# ============================================================
fig, ax = plt.subplots(figsize=(6, 6))

# Farm
ax.plot([0, 100, 100, 0, 0], [0, 0, 100, 100, 0], 'k-', linewidth=2)

# River
ax.fill_between([-5, 0], -5, 105, color='#64B5F6', alpha=0.5)

# Trunk pipe (red thick)
ax.plot([0, 0], [0, 100], color='#C62828', linewidth=3, label='主干管 (100m)')

# Branch pipes
cols = [25, 50, 75]
rows = [7.5 + i*15 for i in range(7)]
for cy in rows:
    ax.plot([0, 75], [cy, cy], color='#1976D2', linewidth=1.2, alpha=0.7)
    for cx in cols:
        ax.plot(cx, cy, 'o', color='#1976D2', markersize=5)

# Coverage circles for a few
for cx in [25, 50, 75]:
    for cy in [7.5, 52.5, 97.5]:
        circle = plt.Circle((cx, cy), 15, fill=True, color='#E3F2FD', alpha=0.3, linewidth=0.3)
        ax.add_patch(circle)

# Tank
ax.plot(50, 50, 's', color='#FF8F00', markersize=12, markeredgecolor='#E65100', markeredgewidth=1.5)
ax.text(50, 54, '储水罐', ha='center', fontsize=7, color='#E65100')

ax.set_xlim(-8, 108)
ax.set_ylim(-5, 105)
ax.set_xlabel('x (m)', fontsize=9)
ax.set_ylabel('y (m)', fontsize=9)
ax.set_title('图2 灌溉系统管道拓扑与喷头覆盖范围示意图', fontsize=11, fontweight='bold')
ax.legend(loc='upper left', fontsize=7)
ax.set_aspect('equal')
fig.tight_layout(pad=1.0)
fig.savefig(out_dir / 'fig2_pipe_layout.png', dpi=300)
plt.close(fig)
print("[OK] fig2_pipe_layout.png")

# ============================================================
# Fig 3: Soil moisture time series
# ============================================================
try:
    import pandas as pd
    df = pd.read_excel(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\data\soil_moisture.xlsx")
    dates = pd.to_datetime(df.iloc[:, 0])
    sm5 = df.iloc[:, 1].values
    
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(dates, sm5, color='#0F4D92', linewidth=1.0, label='5cm土壤湿度')
    ax.axhline(y=0.22, color='#B64342', linestyle='--', linewidth=1.0, label='最低存活标准 (0.22)')
    ax.fill_between(dates, 0, sm5, alpha=0.15, color='#0F4D92')
    
    ax.set_xlabel('日期', fontsize=9)
    ax.set_ylabel('绝对湿度', fontsize=9)
    ax.set_title('图3 2020年8月至2021年12月 5cm土壤湿度时序变化', fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, loc='upper right')
    fig.tight_layout(pad=1.0)
    fig.savefig(out_dir / 'fig3_soil_moisture.png', dpi=300)
    plt.close(fig)
    print("[OK] fig3_soil_moisture.png")
except Exception as e:
    print(f"[WARN] fig3 failed: {e}")

# ============================================================
# Fig 4: Monthly water demand vs supply
# ============================================================
months = ['5月', '6月', '7月']
demand = [59871, 98060, 91419]
supply = [96735, 96735, 96735]
colors_d = ['#8BCF8B', '#B64342', '#8BCF8B']

fig, ax = plt.subplots(figsize=(6, 4))
x = np.arange(len(months))
width = 0.35
bars1 = ax.bar(x - width/2, demand, width, label='日均需水量', color=colors_d, edgecolor='white')
bars2 = ax.bar(x + width/2, supply, width, label='系统日供水量', color='#0F4D92', alpha=0.7, edgecolor='white')

# Add value labels
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, f'{bar.get_height():.0f}', ha='center', fontsize=7)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, f'{bar.get_height():.0f}', ha='center', fontsize=7)

ax.axhline(y=96735, color='#0F4D92', linestyle=':', linewidth=0.8, alpha=0.5)
ax.set_xticks(x)
ax.set_xticklabels(months)
ax.set_ylabel('水量 (L/日)', fontsize=9)
ax.set_title('图4 各月灌溉需水量与系统供水能力对比', fontsize=11, fontweight='bold')
ax.legend(fontsize=8)
fig.tight_layout(pad=1.0)
fig.savefig(out_dir / 'fig4_monthly_water.png', dpi=300)
plt.close(fig)
print("[OK] fig4_monthly_water.png")

print("\nAll figures regenerated with Chinese labels")

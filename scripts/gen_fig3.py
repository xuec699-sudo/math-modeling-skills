import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

f = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\data\该地土壤湿度数据.xlsx"
df = pd.read_excel(f, sheet_name='JingYueTan')
print("Shape:", df.shape)
print("Columns:", list(df.columns[:10]))
print(df.head(3))

# Generate fig3
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Use first column as date, 2nd as SM5
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

out = Path(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\latex\images\fig3_soil_moisture.png")
fig.savefig(out, dpi=300)
plt.close(fig)
print(f"[OK] fig3_soil_moisture.png saved ({out.stat().st_size} bytes)")

import pandas as pd
f = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\data\该地土壤湿度数据.xlsx"
df = pd.read_excel(f)
print("Columns:", list(df.columns[:8]))
print("First 5 rows:")
print(df.head())
print(f"Shape: {df.shape}")

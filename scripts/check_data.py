import pandas as pd
df = pd.read_excel(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\data\soil_moisture.xlsx")
print("Columns:", list(df.columns[:5]))
print("First 5 rows:")
print(df.head())
print(f"Shape: {df.shape}")

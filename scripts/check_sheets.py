import pandas as pd
# Try all sheets
f = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\data\该地土壤湿度数据.xlsx"
xl = pd.ExcelFile(f)
print("Sheets:", xl.sheet_names)
for s in xl.sheet_names:
    df = pd.read_excel(f, sheet_name=s)
    print(f"\nSheet '{s}': {df.shape}")
    print(df.head(2))
    break  # just first sheet

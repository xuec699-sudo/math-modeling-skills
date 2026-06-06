# 数据预处理与探索性分析模板 (EDA Template)

> 每次拿到赛题数据后，按此模板进行标准化预处理。做完直接填入对应问题的建模阶段。

---

## 1. 数据概览

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 加载数据
df = pd.read_excel("data/附件1.xlsx")  # 替换为实际文件名

print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(df.dtypes)
print(df.describe())
```

**记录：**
- 数据量：[行数] 条记录，[列数] 个变量
- 变量类型：数值 [N] 个，分类 [M] 个
- 时间范围：[起始] ~ [结束]

---

## 2. 缺失值与异常值

```python
# 缺失值统计
missing = df.isnull().sum()
print(f"缺失比例 > 10%:\n{missing[missing > len(df)*0.1]}")

# 异常值检测 (IQR 方法)
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
outliers = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).sum()
print(f"异常值统计:\n{outliers[outliers > 0]}")
```

**处理方案：**
- 缺失率 < 5%：均值/中位数填充 或 线性插值
- 缺失率 5%-20%：多重插补（MICE）或模型预测填充
- 缺失率 > 20%：删除该变量 或 作为独立类别
- 异常值：3σ 原则 或 IQR 方法剔除

---

## 3. 描述性统计与分布

```python
# 数值变量分布
df.hist(figsize=(12, 8), bins=30)
plt.tight_layout()
plt.savefig("output/figures/data_distribution.png", dpi=150)

# 相关性矩阵
corr = df.corr()
plt.figure(figsize=(10, 8))
plt.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns, rotation=90)
plt.yticks(range(len(corr)), corr.columns)
plt.savefig("output/figures/correlation_matrix.png", dpi=150)
```

**关键发现：**
- 强相关变量（|r| > 0.7）：[列出]
- 偏态分布变量：[列出] → 需 log/Box-Cox 变换

---

## 4. 多重共线性诊断

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# VIF 诊断（适用于回归类问题）
X = df.select_dtypes(include=[np.number]).dropna()
vif = pd.DataFrame({
    "Variable": X.columns,
    "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
print(vif.sort_values("VIF", ascending=False))
```

**处理：** VIF > 10 的变量 → 删除或 PCA 降维

---

## 5. 数据预处理流水线

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

# 标准化 / 归一化
scaler = StandardScaler()  # 或 MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 训练/测试拆分
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# 保存处理后的数据
np.savez("output/processed_data.npz",
         X_train=X_train, X_test=X_test,
         y_train=y_train, y_test=y_test)
```

---

## 6. 预处理检查清单

- [ ] 缺失值已处理（记录填充方法）
- [ ] 异常值已检测并处理（记录剔除数量）
- [ ] 变量分布已检查（偏态变量已变换）
- [ ] 多重共线性已诊断（VIF < 10）
- [ ] 数据已标准化/归一化
- [ ] 训练/测试集已拆分并保存
- [ ] 所有处理步骤已记录（可复现）

---

## 7. 输出物

| 文件 | 说明 |
|------|------|
| `output/figures/data_distribution.png` | 数据分布图 |
| `output/figures/correlation_matrix.png` | 相关性矩阵 |
| `output/processed_data.npz` | 预处理后的数据 |
| `output/eda_report.md` | 本报告 |

---

> **提示：** 完成 EDA 后，将关键发现填入各子问题的建模章节。
> 每个子问题的数据预处理差异在对应模型代码中单独处理。

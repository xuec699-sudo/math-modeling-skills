# 数学建模 Skill 标准化提示词

## 快速模板（复制粘贴，替换 `[...]`）

```
使用 math-modeling-contest skill（v5.3.3），求解以下赛题：

【赛题信息】
- 比赛名称：[亚太赛2025 / 51MCM2026 / CUMCM2025]
- 题目编号：[A / B / C]
- 子问题数：[3 / 4 / 5]
- 赛题数据路径：[D:\桌面\待分类\数模比赛\XXX\]

【工作模式】
- 运行模式：[AP全自动 / Manual人工检查点]
- 输出格式：[Word / LaTeX PDF / 两者都要]

【核心要求】
1. 先创建独立工作区：setup_workspace.py --name "[比赛名]_[题号]_[简称]"
2. 把赛题数据拷入 data/ 目录
3. 跑完整 pipeline：问题分析 → 文献调研 → 数据预处理 → 建模求解 → 论文写作 → 审阅修订
4. IRON RULE：每个子问题必须明确模型类型 + 完整数学推导 + 变量定义表
5. 论文生成用 build_docx.py（Word）或 docx_to_latex.py --cleanup（LaTeX PDF）
6. 完成后运行 cleanup_workspace.py 清理中间文件
7. 最终结果见 CODE_MAP.md，标明每个问题对应的代码和算法

【特别注意】
- 图表用中文标注
- 公式编号规范
- 参考文献 >= 10 条
- 论文字数 >= 15000 字符
```

## 精简模板（日常快速调用）

```
@math-modeling-contest 求解 [比赛名] [题号]，数据在 [路径]，
用 AP 模式跑全流程，输出 LaTeX PDF + Word，跑完自动清理。
```

## 分步模板（逐步控制）

```
步骤1: 创建 [比赛名]_[题号] 工作区，导入数据
步骤2: 分析赛题，确定每个子问题的模型思路
步骤3: 对问题1/2/3分别建模求解，完成验证
步骤4: 生成论文（Word 初稿）
步骤5: 人工审阅修订
步骤6: 转换为 LaTeX PDF，清理 + 生成 CODE_MAP
```

## 实际例子

### 亚太赛 A 题
```
使用 math-modeling-contest skill（v5.3.3）求解：

赛题：亚太赛2025 A题 农业灌溉系统优化
数据：D:\桌面\待分类\数模比赛\亚太赛2025数模\A题\
模式：AP全自动
输出：LaTeX PDF + Word，跑完自动清理

先创建 contests/APMCM2025_A_农业灌溉/ 工作区，
然后跑完整 6 阶段 pipeline。
```

### 51MCM C 题
```
@math-modeling-contest 求解 51MCM2026 C题（边坡预警），
用 Manual 模式，每个子问题建模后等我确认再继续，
最终输出 Word 论文。
```

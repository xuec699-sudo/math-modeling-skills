import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read main file
with open(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\draft_paper_v2.md", 'r', encoding='utf-8') as f:
    content = f.read()

# Read new section
with open(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\section_42_new.md", 'r', encoding='utf-8') as f:
    new_section = f.read()

old_start = content.find("### 4.2 模型二")
old_end = content.find("### 4.3 模型三")
content = content[:old_start] + new_section + "\n\n" + content[old_end:]

# Update abstract
old_abs = '其次，以2021年7月实际气象数据为基础，建立以总建设成本最小化为目标的灌溉管网优化模型。考虑喷头覆盖半径为15m且间距不小于15m的约束条件，在100m×100m的农场内采用3列7行的网格化布局，共配置21个旋转喷头（理论覆盖面积14,844m²，因重叠覆盖有效覆盖约10,000m²）。依据管道成本函数$C=50L^{1.2}+0.1Q^{1.5}$，分别计算了主干管（长100m，日流量96,735L）与21根支管（总长1,050m）的建设费用，管道总成本为15,398,611。配置容积为193,471L的中央储水罐（提供两日灌溉缓冲），储水罐建设成本为967,355。系统总建设成本为16,365,966。'
new_abs = '其次，以2021年7月实际气象数据为基础，建立以总建设成本最小化为目标的灌溉管网优化模型。将问题形式化为包含8类决策变量和6类约束的混合整数非线性规划（MINLP），采用结构化枚举法在5种候选网格布局中搜索最优解。最终选定3列x7行网格布局（21个旋转喷头），管道总成本15,301,846，配置193,470L中央储水罐（成本967,350），系统总建设成本16,269,196。优化过程包含完整的模型推导、约束验证和方案对比，求解逻辑清晰可追溯。'
content = content.replace(old_abs, new_abs)

# Update conclusion
old_conc = '灌溉管网经网格与三角方案对比后选择3x7矩形网格布局，管道总成本15,395,921，加上储水罐的总系统建设成本为16,363,271。'
new_conc = '灌溉管网经结构化枚举法在5种候选布局中搜索最优解，选定3x7网格布局（管道成本15,301,846，储水罐967,350），总系统建设成本16,269,196。'
content = content.replace(old_conc, new_conc)

# Update buffer table
content = content.replace('2(基准) | 193,470 | 967,350 | 16,363,271', '2(基准) | 193,470 | 967,350 | 16,269,196')
content = content.replace('| 1 | 96,735 | 483,675 | 15,879,596', '| 1 | 96,735 | 483,675 | 15,785,521')

with open(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\draft_paper_v3.md", 'w', encoding='utf-8') as f:
    f.write(content)

print(f"New markdown: {len(content)} chars")
print(f"Section 4.2: {len(new_section)} chars")
print("Saved: draft_paper_v3.md")

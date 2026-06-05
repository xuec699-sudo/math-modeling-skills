# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\paper_text_r3.txt", 'r', encoding='utf-8') as f:
    text = f.read()

# Quick scan for key additions
checks = [
    "6.3倍",
    "系统性漂移",
    "R²≈0.91",
    "超参数配置",
    "200棵树",
    "三角交错排列",
    "结构化比较",
    "[10] Wolanin",
    "[11] 张宝忠",
    "[12] Chen T",
    "设计与成本估算",
    "重叠校正",
    "供水-需求平衡方程严格推导",
]

print("Content scan:")
for c in checks:
    count = text.count(c)
    print(f"  {'✓' if count > 0 else '✗'} '{c}': found {count} time(s)")

# Print the CV gap paragraph
import re
match = re.search(r'(.{0,50}6\.3倍.{0,500})', text)
if match:
    print(f"\n--- CV gap discussion excerpt ---")
    print(match.group(1)[:500])

match2 = re.search(r'(.{0,30}三角交错.{0,300})', text)
if match2:
    print(f"\n--- Layout comparison excerpt ---")
    print(match2.group(1)[:400])

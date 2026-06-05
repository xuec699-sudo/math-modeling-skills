import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\draft_paper_v2.md", 'r', encoding='utf-8') as f:
    content = f.read()

# Find section 4.2
start = content.find("### 4.2 模型二")
end = content.find("### 4.3 模型三")
if end == -1:
    end = content.find("### 4.3")

if start >= 0:
    section = content[start:end]
    print(section)
    print(f"\n--- Section 4.2 length: {len(section)} chars ---")

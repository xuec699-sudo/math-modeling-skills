# Verify current version before packing
with open(r"D:\Codex\skills\math-modeling-contest\SKILL.md", 'r', encoding='utf-8') as f:
    for line in f:
        if 'version:' in line:
            print(f"Current version: {line.strip()}")
            break

import zipfile, os

z = zipfile.ZipFile(r"D:\Codex\skills\math-modeling-contest-v5.3.3.zip", "r")
names = z.namelist()
z.close()

# Count by category
cats = {}
for n in names:
    parts = n.replace("\\", "/").split("/")
    top = parts[0] if len(parts) > 0 else "root"
    cats[top] = cats.get(top, 0) + 1

print("math-modeling-contest v5.3.3")
print(f"Files: {len(names)}  |  Size: {os.path.getsize(r'D:\Codex\skills\math-modeling-contest-v5.3.3.zip')/1024/1024:.1f} MB\n")
for k in sorted(cats.keys()):
    print(f"  {k}/  ({cats[k]} files)")

# Key files check
keys = ["SKILL.md", "build_docx.py", "quality_gate.py", "pipeline_manager.py"]
for k in keys:
    found = any(k in n for n in names)
    print(f"  {'V' if found else 'X'} {k}")

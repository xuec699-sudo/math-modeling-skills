import zipfile, os
path = r"D:\Codex\skills\math-modeling-contest-v5.3.3.zip"
z = zipfile.ZipFile(path)
names = z.namelist()
z.close()

cats = {}
for n in names:
    top = n.replace("\\", "/").split("/")[0]
    cats[top] = cats.get(top, 0) + 1

size_mb = os.path.getsize(path) / 1024 / 1024
print("math-modeling-contest v5.3.3")
print("Files: {} | Size: {:.1f} MB".format(len(names), size_mb))
print()
for k in sorted(cats.keys()):
    print("  {}/  ({} files)".format(k, cats[k]))
print()
for k in ["SKILL.md", "build_docx.py", "quality_gate.py", "pipeline_manager.py", "paper_final_v3.docx"]:
    found = any(k in n for n in names)
    print("  {} {}".format("V" if found else "X", k))

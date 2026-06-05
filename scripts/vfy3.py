import zipfile, os
path = r"D:\Codex\skills\math-modeling-contest-v5.3.3.zip"
z = zipfile.ZipFile(path)
names = z.namelist()
z.close()

# Check directory structure
top_dirs = set()
for n in names:
    parts = n.replace("\\", "/").split("/")
    if len(parts) >= 1:
        top_dirs.add(parts[0])

size_mb = os.path.getsize(path) / 1024 / 1024
print("math-modeling-contest v5.3.3")
print("Files: {} | Size: {:.1f} MB".format(len(names), size_mb))
print()
for d in sorted(top_dirs):
    count = sum(1 for n in names if n.startswith(d))
    print("  {}/  ({} files)".format(d, count))

# Verify key files
print()
for k in ["SKILL.md", "scripts/build_docx.py", "scripts/quality_gate.py", 
          "scripts/pipeline_manager.py", "CUMCM_Workspace/output/paper_final_v3.docx"]:
    found = any(n.endswith(k) for n in names)
    print("  {} {}".format("V" if found else "X", k))

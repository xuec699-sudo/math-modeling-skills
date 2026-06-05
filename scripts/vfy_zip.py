import zipfile, os

z = zipfile.ZipFile(r"D:\Codex\skills\math-modeling-contest.zip", "r")
names = z.namelist()
z.close()

top = set(n.split("/")[0] for n in names if "/" in n)
scripts = [n for n in names if n.endswith(".py") and "scripts/" in n]
refs = [n for n in names if "references/" in n]
papers = [n for n in names if "paper_final" in n]
size_mb = os.path.getsize(r"D:\Codex\skills\math-modeling-contest.zip") / 1024 / 1024

print(f"Size: {size_mb:.1f} MB")
print(f"Files: {len(names)} total")
print(f"\nTop-level: {sorted(top)}")
print(f"Scripts: {len(scripts)} .py")
print(f"References: {len(refs)}")
print(f"Papers: {len(papers)} (v3 final)")
print(f"\nKey files:")
for f in sorted(names):
    name = f.split("/")[-1]
    if name in ["SKILL.md", "build_docx.py", "quality_gate.py", "paper_final_v3.docx"]:
        print(f"  {f}")

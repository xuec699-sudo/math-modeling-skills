import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Patch 1: Add #### handler after ### handler
old1 = '''if line.startswith("### "):
            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(8)
            r = p.add_run(line[4:]); set_font(r, 12, True, "\u9ed1\u4f53"); i += 1; continue
        if line.startswith("# "):'''

new1 = '''if line.startswith("### "):
            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(8)
            r = p.add_run(line[4:]); set_font(r, 12, True, "\u9ed1\u4f53"); i += 1; continue
        if line.startswith("#### "):
            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)
            r = p.add_run(line[5:]); set_font(r, 12, True, "\u5b8b\u4f53"); i += 1; continue
        if line.startswith("# "):'''

if old1 in content:
    content = content.replace(old1, new1)
    print("[OK] Patch 1: #### handler added")
else:
    print("[FAIL] Patch 1: old text not found")

# Patch 2: Add --- and ``` handlers after skip-empty block
old2 = '''# Skip empty
        if not line: i += 1; continue

        # Heading'''

new2 = '''# Skip empty
        if not line: i += 1; continue

        # Horizontal rule / separator - skip silently
        if line.strip() in ("---", "***", "___"):
            i += 1; continue

        # Code fence - skip silently
        if line.strip().startswith("```"):
            i += 1; continue

        # Heading'''

if old2 in content:
    content = content.replace(old2, new2)
    print("[OK] Patch 2: --- and ``` handlers added")
else:
    print("[FAIL] Patch 2: old text not found")
    # Debug: show what's around "Skip empty"
    idx = content.find("Skip empty")
    if idx >= 0:
        print(f"  Context: {repr(content[idx:idx+100])}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    vfy = f.read()
for name, term in [("#### handler", 'line.startswith("#### ")'), ("--- handler", '("---"'), ("fence handler", "startswith(\"```\")")]:
    print(f"  '{name}': {'FOUND' if term in vfy else 'MISSING'}")

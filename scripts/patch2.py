import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Insert #### handler after ### handler  
for i, line in enumerate(lines):
    if line.rstrip() == 'if line.startswith("### "):':
        j = i + 1
        while j < len(lines) and (lines[j].startswith('            ') or lines[j].strip() == ''):
            j += 1
        insert = [
            '        if line.startswith("#### "):\n',
            '            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)\n',
            '            r = p.add_run(line[5:]); set_font(r, 12, True, "\u5b8b\u4f53"); i += 1; continue\n',
        ]
        for k, ins in enumerate(insert):
            lines.insert(j + k, ins)
        print(f"[OK] Inserted #### handler")
        break

# 2. Insert --- and ``` handlers after "Skip empty" block
for i, line in enumerate(lines):
    stripped = line.rstrip()
    if stripped == '# Skip empty' and i+1 < len(lines) and 'if not line:' in lines[i+1]:
        j = i + 2
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        # j should be at "# Heading" now
        insert = [
            '\n',
            '        # Horizontal rule / separator - skip silently\n',
            '        if line.strip() in ("---", "***", "___"):\n',
            '            i += 1; continue\n',
            '\n',
            '        # Code fence - skip silently\n',
            '        if line.strip().startswith("```"):\n',
            '            i += 1; continue\n',
        ]
        for k, ins in enumerate(insert):
            lines.insert(j + k, ins)
        print(f"[OK] Inserted --- and ``` handlers")
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

checks = ['####', '---', 'Code fence']
for c in checks:
    found = c in content
    print(f"  Verify '{c}': {'OK' if found else 'MISSING'}")

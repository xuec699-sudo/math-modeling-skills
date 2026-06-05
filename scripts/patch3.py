import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Insert in reverse order so line numbers stay valid

# Patch 1: After line 186 (### handler block), insert #### handler
# Original lines 184-186:
#         if line.startswith("### "):
#             p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(8)
#             r = p.add_run(line[4:]); set_font(r, 12, True, "黑体"); i += 1; continue
# Line 187:         if line.startswith("# "):
insert_at = 186  # 0-indexed, after the ### block's "continue" line

new_lines1 = [
    '        if line.startswith("#### "):\n',
    '            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)\n',
    '            r = p.add_run(line[5:]); set_font(r, 12, True, "\u5b8b\u4f53"); i += 1; continue\n',
    '\n',
]
for k, nl in enumerate(reversed(new_lines1)):
    lines.insert(insert_at + 1, nl)

print(f"[OK] Inserted #### handler after line {insert_at+1}")

# Patch 2: After lines 178-179 (skip empty block), insert --- and ``` handlers
# Original lines:
# 177:         # Skip empty
# 178:         if not line: i += 1; continue
# 179: (empty)
# 180:         # Heading
# Insert between 179 and 180

# Re-find the insertion point (line numbers shifted after first insert)
for i, line in enumerate(lines):
    if line.rstrip() == '# Heading':
        insert_at = i - 1  # insert before "# Heading"
        new_lines2 = [
            '\n',
            '        # Horizontal rule / separator - skip silently\n',
            '        if line.strip() in ("---", "***", "___"):\n',
            '            i += 1; continue\n',
            '\n',
            '        # Code fence - skip silently\n',
            '        if line.strip().startswith("```"):\n',
            '            i += 1; continue\n',
        ]
        for k, nl in enumerate(reversed(new_lines2)):
            lines.insert(insert_at + 1, nl)
        print(f"[OK] Inserted --- and ``` handlers before line {i+1}")
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

checks = ['####', 'Horizontal rule', 'Code fence']
all_ok = True
for c in checks:
    ok = c in content
    print(f"  '{c}': {'FOUND' if ok else 'MISSING'}")
    if not ok: all_ok = False

if all_ok:
    print("\n[DONE] build_docx.py patched successfully")
else:
    print("\n[FAIL] Some patches missing")

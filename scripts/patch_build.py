# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Find the heading handling section
for i, line in enumerate(lines):
    if line.strip().startswith('if line.startswith("### "):'):
        # Found the ### handler. Insert #### handler after this block
        # Find where this if-block ends (next line that's not indented more)
        j = i
        while j < len(lines):
            if lines[j].strip() == 'if line.startswith("### "):':
                j += 1
                while j < len(lines) and (lines[j].startswith('            ') or lines[j].strip() == ''):
                    j += 1
                break
            j += 1
        # j is now at the line after the ### block
        insert_lines = [
            '        if line.startswith("#### "):',
            '            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)',
            '            r = p.add_run(line[5:]); set_font(r, 12, True, "宋体"); i += 1; continue'
        ]
        for k, ins in enumerate(insert_lines):
            lines.insert(j + k, ins)
        print(f"Inserted #### handler after line {j-1}")
        break

# Find "Skip empty" and add --- and ``` handlers
for i, line in enumerate(lines):
    if '# Skip empty' in line and 'if not line:' in lines[i+1]:
        # Find the end of the skip-empty block
        j = i + 1
        while j < len(lines) and ('if not line:' in lines[j] or 'i += 1; continue' in lines[j]):
            j += 1
        insert_lines = [
            '',
            '        # Horizontal rule / separator — skip silently',
            '        if line.strip() in (\"---\", \"***\", \"___\"):',
            '            i += 1; continue',
            '',
            '        # Code fence — skip silently',
            '        if line.strip().startswith(\"```\"):',
            '            i += 1; continue',
        ]
        for k, ins in enumerate(insert_lines):
            lines.insert(j, ins)
        print(f"Inserted --- and ``` handlers after line {j-1}")
        break

with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Patched successfully")

# Verify
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
print(f"  '####' found: {'####' in content}")
print(f"  '--- handler' found: {'---\"' in content}")
print(f"  'Code fence' found: {'Code fence' in content}")

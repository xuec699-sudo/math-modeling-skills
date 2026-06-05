import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Compare backup vs current
with open(r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py.bak", 'r', encoding='utf-8') as f:
    bak = f.read()
with open(r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py", 'r', encoding='utf-8') as f:
    cur = f.read()

bak_lines = set(bak.split('\n'))
cur_lines = set(cur.split('\n'))

only_in_cur = cur_lines - bak_lines
only_in_bak = bak_lines - cur_lines

print("Lines ONLY in CURRENT (my patches):")
for line in sorted(only_in_cur):
    s = line.strip()
    if s:
        print(f"  + {s[:100]}")

print(f"\nLines ONLY in BACKUP (potentially lost):")
for line in sorted(only_in_bak):
    s = line.strip()
    if s:
        print(f"  - {s[:100]}")

# Check if _add_table_cell_text is anywhere
if '_add_table_cell_text' in bak:
    print("\n[FOUND] _add_table_cell_text in backup!")
else:
    print("\n[NOT FOUND] _add_table_cell_text not in backup either")

# Check file sizes
print(f"\nBackup: {len(bak)} chars")
print(f"Current: {len(cur)} chars")
print(f"Delta: {len(cur) - len(bak)} chars")

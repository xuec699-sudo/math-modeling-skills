import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Search for how table cell formulas are handled
# Look for any reference to $ in the table handling code
import re

# Find add_three_line_table function
start = content.find("def add_three_line_table")
end = content.find("\ndef ", start + 1)
if end == -1:
    end = len(content)

table_fn = content[start:end]
print("add_three_line_table function:")
print("=" * 50)
print(table_fn[:2000])
print("..." if len(table_fn) > 2000 else "")
print(f"\nTotal function length: {len(table_fn)} chars")

# Check if there's ANY inline equation handling in tables
if '$' in table_fn and ('omml' in table_fn.lower() or 'latex' in table_fn.lower()):
    print("\n[FOUND] Table has inline equation handling")
else:
    print("\n[NOT FOUND] No inline equation handling in table function")
    print("Tables just do: r = p.add_run(str(val))")

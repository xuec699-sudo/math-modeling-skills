with open("build_docx.py", "r", encoding="utf-8") as f:
    content = f.read()

changes = 0

# Revert margins
if "Cm(2.5); s.bottom_margin = Cm(2.5)" in content:
    content = content.replace("Cm(2.5); s.bottom_margin = Cm(2.5)", "Cm(2.54); s.bottom_margin = Cm(2.54)")
    changes += 1
if "Cm(3.2); s.right_margin = Cm(3.2)" in content:
    content = content.replace("Cm(3.2); s.right_margin = Cm(3.2)", "Cm(3.18); s.right_margin = Cm(3.18)")
    changes += 1

# Revert table fonts: 10.5 -> 9
for old, new in [
    ("font_size=10.5, bold=True", "font_size=9, bold=True"),
    ("font_size=10.5)\n", "font_size=9)\n"),  # data cell call
]:
    if old in content:
        content = content.replace(old, new)
        changes += 1

# Revert Pt(10.5) that was changed for table purposes, 
# but be careful not to revert Pt(10.5) in non-table contexts
# The pattern: "Pt(9)" was replaced with "Pt(10.5)" earlier
# Let's find table-related Pt(10.5) and revert
# In add_three_line_table context, there are these Pt references
for old_pt, new_pt in [
    ('r.font.size = Pt(10.5); r.font.bold = True', 'r.font.size = Pt(9); r.font.bold = True'),
]:
    if old_pt in content:
        content = content.replace(old_pt, new_pt)
        changes += 1

# Also revert Pt(10.5) in set_font calls for captions
for old_sf, new_sf in [
    ("set_font(r, 10.5)", "set_font(r, 10)"),
    ("set_font(rc, 10.5)", "set_font(rc, 10)"),
]:
    if old_sf in content:
        content = content.replace(old_sf, new_sf)
        changes += 1

# Remove heading style setup if present
marker = "# Configure heading styles per template"
if marker in content:
    # Find the block
    idx = content.find(marker)
    # Find end of the block (next empty line after the block)
    end = content.find("\n    i = 0", idx)
    if end < 0:
        end = content.find("\n    #", idx)
    if end > idx:
        content = content[:idx-1] + content[end:]  # -1 to remove leading space
        changes += 1

with open("build_docx.py", "w", encoding="utf-8") as f:
    f.write(content)

import py_compile
py_compile.compile("build_docx.py", doraise=True)
print(f"Reverted {changes} format changes. Syntax OK.")

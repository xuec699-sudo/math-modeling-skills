import re

with open("build_docx.py", "r", encoding="utf-8") as f:
    content = f.read()

changes = 0

# 1. Page margins: match template (2.5cm all sides, 3.2cm left/right)
old = "s.top_margin = Cm(2.54); s.bottom_margin = Cm(2.54)"
new = "s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5)"
if old in content:
    content = content.replace(old, new)
    changes += 1

old = "s.left_margin = Cm(3.18); s.right_margin = Cm(3.18)"
new = "s.left_margin = Cm(3.2); s.right_margin = Cm(3.2)"
if old in content:
    content = content.replace(old, new)
    changes += 1

# 2. Table cell font: 9pt -> 10.5pt (五号)
content = content.replace("font_size=9, bold=True", "font_size=10.5, bold=True")
content = content.replace("font_size=9)", "font_size=10.5)")
content = content.replace("Pt(9)", "Pt(10.5)")  # General font size in tables
changes += 1

# 3. Table caption font: Pt(10) -> Pt(10.5)
content = content.replace('r.font.size = Pt(10); r.font.bold = True', 'r.font.size = Pt(10.5); r.font.bold = True')
changes += 1

# 4. Figure caption font: Pt(10) -> Pt(10.5), source code Pt(10) -> Pt(10.5)
# Already handled by Pt(9) -> Pt(10.5) but let's check remaining Pt(10)
content = content.replace('set_font(r, 10)', 'set_font(r, 10.5)')
content = content.replace('set_font(rc, 10)', 'set_font(rc, 10.5)')
changes += 1

# 5. Body text font: ensure 12pt for set_font calls
# set_font(r, 12, ...) stays as is (小四=12pt)

# 6. Add heading style setup before document processing
# Find "doc = Document()" and add style config after
style_setup = '''
    # Configure heading styles per template
    for lvl, sz in [(1, 14), (2, 13), (3, 12)]:
        style = doc.styles[f"Heading {lvl}"]
        style.font.size = Pt(sz)
        style.font.bold = True
        style.font.name = "Times New Roman"
        style.element.rPr.rFonts.set(qn("w:eastAsia"), "黑体")
    # Normal style for body
    ns = doc.styles["Normal"]
    ns.font.size = Pt(12)
    ns.font.name = "Times New Roman"
    ns.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    ns.paragraph_format.line_spacing = 1.5
'''
if "doc.styles" not in content and "doc = Document()" in content:
    content = content.replace("doc = Document()", "doc = Document()" + style_setup)
    changes += 1

# 7. Fix line spacing for body paragraphs
old_ls = "p.paragraph_format.line_spacing = 1.5"
if old_ls in content:
    changes += 0  # Already correct

with open("build_docx.py", "w", encoding="utf-8") as f:
    f.write(content)

import py_compile
py_compile.compile("build_docx.py", doraise=True)
print(f"Applied {changes} format changes. Syntax OK.")

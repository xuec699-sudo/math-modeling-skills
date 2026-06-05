with open("build_docx.py", "r", encoding="utf-8") as f:
    content = f.read()

# A4 page size
old = "s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5)"
new = "s.page_width = Cm(21.0)\n        s.page_height = Cm(29.7)\n        s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5)"
content = content.replace(old, new)
print("Added A4 page size")

# Add font to _add_table_cell_text - text segments
old_txt = "r = para.add_run(seg)\n                r.font.size = Pt(font_size)\n                r.font.bold = bold"
new_txt = 'r = para.add_run(seg)\n                r.font.name = "Times New Roman"\n                r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")\n                r.font.size = Pt(font_size)\n                r.font.bold = bold'
if old_txt in content:
    content = content.replace(old_txt, new_txt)
    print("Added font to table text runs")
else:
    print("WARNING: text run pattern not found")

# Add font to equation fallback runs  
old_fb = 'r = para.add_run(f"${seg}$")\n                r.font.size = Pt(font_size)\n                r.font.bold = bold'
new_fb = 'r = para.add_run(f"${seg}$")\n                r.font.name = "Times New Roman"\n                r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")\n                r.font.size = Pt(font_size)\n                r.font.bold = bold'
if old_fb in content:
    content = content.replace(old_fb, new_fb)
    print("Added font to equation fallback runs")
else:
    print("WARNING: fallback pattern not found")

with open("build_docx.py", "w", encoding="utf-8") as f:
    f.write(content)

import py_compile
py_compile.compile("build_docx.py", doraise=True)
print("Syntax OK")

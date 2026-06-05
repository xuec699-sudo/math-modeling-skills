import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _add_table_cell_text function before add_three_line_table
old_fn_start = "def add_three_line_table(doc, headers, rows, caption_text=None):"

new_fn = '''def _add_table_cell_text(cell, text):
    """Add text to a table cell, converting $...$ inline formulas to OMML."""
    INLINE_EQ = re.compile(r"\\$(.+?)\\$")
    segments = INLINE_EQ.split(str(text))
    
    # Clear cell
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    for k, seg in enumerate(segments):
        if k % 2 == 1:
            # Equation segment - convert to OMML
            omml = latex_to_omml(seg)
            if omml:
                inject_omml(p, omml)
            else:
                r = p.add_run("$" + seg + "$")
                r.font.name = "Times New Roman"
                r._element.rPr.rFonts.set(qn("w:eastAsia"), "\u5b8b\u4f53")
                r.font.size = Pt(9)
        else:
            # Text segment
            if seg.strip():
                r = p.add_run(seg)
                r.font.name = "Times New Roman"
                r._element.rPr.rFonts.set(qn("w:eastAsia"), "\u5b8b\u4f53")
                r.font.size = Pt(9)

def add_three_line_table(doc, headers, rows, caption_text=None):'''

content = content.replace(old_fn_start, new_fn)

# 2. Replace the data row logic in add_three_line_table to use _add_table_cell_text
old_data = '''    # Data rows
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i+1].cells[j]; cell.text = ""
            p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"; r._element.rPr.rFonts.set(qn("w:eastAsia"),"\u5b8b\u4f53")
            r.font.size = Pt(9)'''

new_data = '''    # Data rows - with inline formula support
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i+1].cells[j]
            _add_table_cell_text(cell, str(val))'''

content = content.replace(old_data, new_data)

# 3. Also apply to header row
old_header = '''    # Header row
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]; cell.text = ""
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"; r._element.rPr.rFonts.set(qn("w:eastAsia"),"\u5b8b\u4f53")
        r.font.size = Pt(9); r.font.bold = True
        # Thin bottom border on header cells
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement("w:tcBorders")
        be = OxmlElement("w:bottom"); be.set(qn("w:val"),"single")
        be.set(qn("w:sz"),"4"); be.set(qn("w:color"),"000000")
        tcBorders.append(be); tcPr.append(tcBorders)'''

new_header = '''    # Header row - with inline formula support
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        _add_table_cell_text(cell, h)
        # Make header bold
        for run in cell.paragraphs[0].runs:
            run.font.bold = True
        # Thin bottom border on header cells
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement("w:tcBorders")
        be = OxmlElement("w:bottom"); be.set(qn("w:val"),"single")
        be.set(qn("w:sz"),"4"); be.set(qn("w:color"),"000000")
        tcBorders.append(be); tcPr.append(tcBorders)'''

content = content.replace(old_header, new_header)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
checks = ['_add_table_cell_text', 'INLINE_EQ.split', 'inject_omml(p, omml)']
for c in checks:
    print(f"  '{c}': {'FOUND' if c in content else 'MISSING'}")

print("\n[DONE] _add_table_cell_text re-implemented in build_docx.py")

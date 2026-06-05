import sys, io, zipfile, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

docx = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\table_test2.docx"
with zipfile.ZipFile(docx, "r") as z:
    xml = z.read("word/document.xml").decode("utf-8", errors="replace")

tcs = re.findall(r"<w:tc>(.*?)</w:tc>", xml, re.DOTALL)
omml = sum(1 for tc in tcs if "<m:oMath" in tc)
raw = sum(1 for tc in tcs if re.search(r"<w:t[^>]*>\$[^<]*\$</w:t>", tc))

print(f"Table cells: {len(tcs)}")
print(f"OMML in table cells: {omml}")
print(f"Raw $ in table cells: {raw}")
print(f"RESULT: {'PASS - all table formulas rendered' if raw == 0 and omml > 0 else 'FAIL'}")

os.remove(docx)

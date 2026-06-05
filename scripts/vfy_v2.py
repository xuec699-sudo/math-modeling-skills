import zipfile, re
docx = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\paper_final_v2.docx"
with zipfile.ZipFile(docx, "r") as z:
    xml = z.read("word/document.xml").decode("utf-8")

omml = len(re.findall(r"<m:oMath", xml))
raw_dollar = len(re.findall(r"<w:t[^>]*>\$[^<]*\$</w:t>", xml))
tcs = re.findall(r"<w:tc>(.*?)</w:tc>", xml, re.DOTALL)
omml_table = sum(1 for tc in tcs if "<m:oMath" in tc)
raw_table = sum(1 for tc in tcs if re.search(r"<w:t[^>]*>\$", tc))

print(f"Total OMML equations: {omml}")
print(f"Raw $ remaining: {raw_dollar}")
print(f"Table cells with OMML: {omml_table}")
print(f"Table cells with raw $: {raw_table}")
print(f"File size: {__import__('os').path.getsize(docx)/1024:.0f} KB")
if raw_dollar == 0:
    print("RESULT: PASS - All formulas rendered correctly")
else:
    print(f"RESULT: FAIL - {raw_dollar} raw formulas remain")

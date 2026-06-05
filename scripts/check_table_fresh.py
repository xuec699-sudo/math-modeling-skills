import sys, io, zipfile, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

docx = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\table_test.docx"
with zipfile.ZipFile(docx, "r") as z:
    xml = z.read("word/document.xml").decode("utf-8", errors="replace")

tcs = re.findall(r"<w:tc>(.*?)</w:tc>", xml, re.DOTALL)
omml = sum(1 for tc in tcs if "<m:oMath" in tc)
raw = sum(1 for tc in tcs if re.search(r"<w:t[^>]*>\$[^<]*\$</w:t>", tc))
raw_text = re.findall(r"<w:t[^>]*>(\$[^<]*?\$)</w:t>", xml)
raw_examples = raw_text[:5]

print(f"Table cells: {len(tcs)}")
print(f"With OMML: {omml}")
print(f"With raw $: {raw}")
print(f"Raw $ examples: {raw_examples}")

os.remove(docx)
print("\nTest file cleaned up")

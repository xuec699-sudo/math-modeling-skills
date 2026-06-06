import sys, io, zipfile, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

docx = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\paper_final_v3.docx"
with zipfile.ZipFile(docx, "r") as z:
    xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    images = [n for n in z.namelist() if "media" in n and n.endswith('.png')]

tcs = re.findall(r"<w:tc>(.*?)</w:tc>", xml, re.DOTALL)
omml_table = sum(1 for tc in tcs if "<m:oMath" in tc)
raw_table = sum(1 for tc in tcs if re.search(r"<w:t[^>]*>\$", tc))
omml_all = len(re.findall(r"<m:oMath", xml))
drawings = len(re.findall(r"<wp:inline|<wp:anchor", xml))

print(f"Size: {os.path.getsize(docx)/1024:.0f} KB")
print(f"Images embedded: {len(images)} ({', '.join([n.split('/')[-1] for n in images])})")
print(f"Drawings in XML: {drawings}")
print(f"Table cells with OMML: {omml_table}")
print(f"Table cells with raw $: {raw_table}")
print(f"Total OMML elements: {omml_all}")
print(f"\nRESULT: {'PASS' if raw_table == 0 and len(images) >= 3 else 'CHECK NEEDED'}")

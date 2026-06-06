import zipfile, re, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_docx(path):
    if not os.path.exists(path):
        return {"path": path, "exists": False}
    size = os.path.getsize(path)
    with zipfile.ZipFile(path, "r") as z:
        names = z.namelist()
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    omml = len(re.findall(r"<m:oMath", xml))
    images = [n for n in names if "image" in n.lower() or n.endswith(('.png','.jpg','.jpeg'))]
    media_images = [n for n in images if "media" in n]
    drawings = len(re.findall(r"<wp:inline|<wp:anchor", xml))
    tables = len(re.findall(r"<w:tbl>", xml))
    raw_dollar = len(re.findall(r"<w:t[^>]*>\$", xml))
    return {
        "file": os.path.basename(path),
        "size_kb": round(size/1024, 1),
        "omml": omml,
        "embedded_images": len(media_images),
        "drawings_in_xml": drawings,
        "tables": tables,
        "raw_dollar": raw_dollar,
    }

base = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output"
for f in ["paper_final.docx", "paper_final_v2.docx"]:
    info = analyze_docx(os.path.join(base, f))
    print(f"{info['file']}: {info['size_kb']}KB | OMML={info['omml']} | Images={info['embedded_images']} | Drawings={info['drawings_in_xml']} | Tables={info['tables']} | Raw$={info['raw_dollar']}")

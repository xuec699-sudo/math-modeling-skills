import zipfile, re, os

def analyze_docx(path):
    if not os.path.exists(path):
        return {"path": path, "exists": False}
    
    size = os.path.getsize(path)
    with zipfile.ZipFile(path, "r") as z:
        names = z.namelist()
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    
    omml = len(re.findall(r"<m:oMath", xml))
    images = [n for n in names if "image" in n.lower() or n.endswith(('.png','.jpg','.jpeg','.gif','.bmp'))]
    drawings = len(re.findall(r"<wp:inline|<wp:anchor", xml))
    tables = len(re.findall(r"<w:tbl>", xml))
    chars = len(re.findall(r"<w:t[^>]*>([^<]+)</w:t>", xml))
    text = "".join(re.findall(r"<w:t[^>]*>([^<]+)</w:t>", xml))
    raw_dollar = len(re.findall(r"<w:t[^>]*>\$", xml))
    
    return {
        "path": os.path.basename(path),
        "size_kb": size/1024,
        "omml": omml,
        "images_in_zip": len(images),
        "image_names": images[:5],
        "drawings": drawings,
        "tables": tables,
        "chars_approx": chars,
        "raw_dollar": raw_dollar,
        "first_200_chars": text[:200]
    }

base = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output"
files = ["paper_final.docx", "paper_final_v2.docx", "paper_template_format.docx"]

for f in files:
    info = analyze_docx(os.path.join(base, f))
    print(f"\n{'='*50}")
    for k, v in info.items():
        print(f"  {k}: {v}")

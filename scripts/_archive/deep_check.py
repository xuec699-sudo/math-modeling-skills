import sys, io, zipfile, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

docx = r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\paper_final.docx"
with zipfile.ZipFile(docx, "r") as z:
    xml = z.read("word/document.xml").decode("utf-8", errors="replace")

# Find ALL table cells
tcs = re.findall(r"<w:tc>(.*?)</w:tc>", xml, re.DOTALL)

omml_in_table = 0
raw_dollar_in_table = 0
examples_raw = []
examples_omml = []

for tc in tcs:
    has_omml = "<m:oMath" in tc
    has_raw = bool(re.search(r"<w:t[^>]*>\$[^<]*\$</w:t>", tc))
    
    if has_omml:
        omml_in_table += 1
        # Extract first few chars of the equation
        omml_text = re.search(r"<m:t[^>]*>(.*?)</m:t>", tc)
        if omml_text and len(examples_omml) < 3:
            examples_omml.append(omml_text.group(1)[:40])
    
    if has_raw:
        raw_dollar_in_table += 1
        dollar_text = re.search(r"<w:t[^>]*>(\$[^<]*\$)</w:t>", tc)
        if dollar_text and len(examples_raw) < 3:
            examples_raw.append(dollar_text.group(1)[:40])

print(f"Table cells total: {len(tcs)}")
print(f"Cells with OMML: {omml_in_table}")
print(f"Cells with raw $: {raw_dollar_in_table}")
print(f"\nOMML examples: {examples_omml}")
print(f"Raw $ examples: {examples_raw}")

# Check: is OMML in table cells actually from equations or from something else?
# Maybe the table cells with $N_s$ etc are rendered as OMML by a DIFFERENT mechanism
# Let me find a specific cell that should have $N_s$ and see how it's stored

# Find cells containing "N_s" or "L_main" in the XML
for tc in tcs:
    if "N_s" in tc or "L_{main}" in tc or "L_main" in tc:
        if "<m:oMath" in tc:
            print(f"\nFOUND: Cell with N_s/L_main AND OMML")
            # Show snippet
            snippet = tc[:500]
            print(f"  XML snippet: {snippet[:300]}...")
            break
        elif "$" in tc:
            # Find the actual text
            matches = re.findall(r"<w:t[^>]*>(.*?)</w:t>", tc)
            for m in matches:
                if "$" in m:
                    print(f"\nFOUND: Cell with raw $: '{m[:60]}'")
                    break
            break

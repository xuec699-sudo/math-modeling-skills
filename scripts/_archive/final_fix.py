import re

with open("build_docx.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find all _preprocess_latex
positions = [m.start() for m in re.finditer("def _preprocess_latex", content)]
print(f"Found {len(positions)} _preprocess_latex functions")

# Remove duplicates (keep only the first one)
for idx in positions[1:]:
    end = content.find("\ndef ", idx + 10)
    if end < 0:
        end = content.find("\n#", idx + 10)
    print(f"Removing duplicate at {idx} to {end}")
    content = content[:idx] + content[end:]

with open("build_docx.py", "w", encoding="utf-8") as f:
    f.write(content)

# Test
import importlib, build_docx
importlib.reload(build_docx)
test = r"\begin{aligned} a &= b \\ c &= d \end{aligned}"
result = build_docx._preprocess_latex(test)
omml = build_docx.latex_to_omml(test)
print(f"Test: {test}")
print(f"Out:  {result}")
has_math = "<m:oMath" in omml if omml else False
print(f"OK:   {has_math}")

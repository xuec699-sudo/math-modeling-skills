import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Show exact line numbers for key patterns
for i, line in enumerate(lines):
    s = line.rstrip()
    if 'line.startswith("### ")' in s:
        print(f"Line {i+1}: {s}")
    if s == '        if line.startswith("## "):':
        print(f"Line {i+1}: {s}")
    if '# Skip empty' in s:
        print(f"Line {i+1}: {s}")
    if '# Heading' in s and i < 185:
        print(f"Line {i+1}: {s}")

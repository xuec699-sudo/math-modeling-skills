import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"D:\Codex\skills\math-modeling-contest\scripts\build_docx.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find("def add_three_line_table")
end = content.find("\ndef ", start + 1)
table_fn = content[start:end]
print(table_fn)

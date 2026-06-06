# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

doc = Document(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\test_clean.docx")

artifacts = 0
for i, para in enumerate(doc.paragraphs):
    t = para.text.strip()
    if t.startswith('#### ') or t == '---' or t == '```':
        print(f"[{i}] ARTIFACT: '{t[:80]}'")
        artifacts += 1

if artifacts == 0:
    print("VERIFIED: 0 markdown artifacts in fresh build ✓")
    print(f"build_docx.py fix is working correctly")
else:
    print(f"FAILED: {artifacts} artifacts remain")

# Clean up test file
import os
os.remove(r"D:\Codex\skills\math-modeling-contest\CUMCM_Workspace\output\test_clean.docx")
print("Test file cleaned up")

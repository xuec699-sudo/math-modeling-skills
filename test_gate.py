import sys, os
sys.path.insert(0, "scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("qg", os.path.abspath("scripts/quality_gate.py"))
qg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qg)

ok, msg = qg.gate_table_formula("CUMCM_Workspace/output/paper_final_v2.docx")
status = "PASS" if ok else "FAIL"
print(f"Table Formula Gate: {status} - {msg}")

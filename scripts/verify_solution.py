import json, os, re, sys
from pathlib import Path
from datetime import datetime

CHECK_TYPES = {
    "baseline": {"name": "Baseline Comparison", "desc": "Compare against simple baseline"},
    "parameter_sensitivity": {"name": "Parameter Sensitivity", "desc": "Perturb key parameters +/-20%"},
    "error_analysis": {"name": "Error Analysis", "desc": "Check residuals and error patterns"},
    "extreme_scenario": {"name": "Extreme Scenario", "desc": "Test at boundary conditions"},
    "weight_sensitivity": {"name": "Weight Sensitivity", "desc": "Perturb weights +/-20%"},
    "data_perturbation": {"name": "Data Perturbation", "desc": "Add noise, delete samples"},
    "random_stability": {"name": "Randomness Stability", "desc": "Test across 10+ seeds"},
    "constraint_perturbation": {"name": "Constraint Perturbation", "desc": "Relax/tighten constraints"},
}

MODEL_CHECKS = {
    "optimization": ["baseline", "parameter_sensitivity", "constraint_perturbation", "extreme_scenario"],
    "prediction": ["baseline", "parameter_sensitivity", "error_analysis", "data_perturbation", "extreme_scenario"],
    "statistics": ["baseline", "parameter_sensitivity", "error_analysis", "data_perturbation"],
    "evaluation": ["baseline", "weight_sensitivity", "parameter_sensitivity"],
    "classification": ["baseline", "parameter_sensitivity", "error_analysis", "data_perturbation"],
    "simulation": ["baseline", "parameter_sensitivity", "random_stability", "extreme_scenario"],
    "mechanism": ["baseline", "parameter_sensitivity", "extreme_scenario"],
}

def check_depth(text):
    score = 0
    issues = []
    for cid, pat, fail in [
        ("type", r"(建立|构建|采用|提出).{0,20}(模型|方法|算法)", "model type not declared"),
        ("vars", r"(其中|式中|令|设|记).{0,30}[a-zA-Z]", "variables not defined"),
        ("fnum", r"\(\d+[a-z]?\)|式\s*\(\d+\)", "formulas not numbered"),
        ("deriv", r"(代入|可得|推导|计算|整理|化简|展开)", "no derivation steps"),
        ("assume", r"(假设|假定|不妨设|考虑|忽略)", "assumptions not stated"),
        ("symtab", r"(符号|变量|参数).{0,10}(表|说明|定义|含义)", "no symbol table"),
    ]:
        if re.search(pat, text):
            score += 1
        else:
            issues.append(fail)
    lvl = "L1" if score <= 1 else "L2" if score <= 3 else "L3" if score <= 5 else "L4"
    return {"score": score, "max": 6, "level": lvl, "issues": issues, "passed": score >= 4}

def main():
    p = __import__("argparse").ArgumentParser(description="Solution Verification Engine")
    p.add_argument("--workspace", default=".")
    p.add_argument("--question", default="Q1")
    p.add_argument("--model-type", default="prediction", choices=list(MODEL_CHECKS))
    p.add_argument("--depth-check", help="Model text or file to check depth")
    args = p.parse_args()

    ws = Path(args.workspace)
    q = args.question
    rob = ws / "robustness" / q
    rob.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    req = MODEL_CHECKS.get(args.model_type, ["baseline"])

    report = f"# {q} Robustness Report\n\nGenerated: {now}\nModel: {args.model_type}\nStatus: pending\n\n"
    report += "## Required Checks\n\n"
    for cid in req:
        c = CHECK_TYPES[cid]
        report += f"- [{c['name']}]: {c['desc']} (pending)\n"
    report += "\n## Baseline Comparison\n\n| Metric | Baseline | Main | Improvement |\n|--------|----------|------|-------------|\n| ? | ? | ? | ? |\n\n"
    report += "## Supported Conclusions\n\n[to determine]\n\n"
    report += "## Fragile Conclusions\n\n[to determine]\n"

    (rob / f"{q.lower()}_robustness_report.md").write_text(report, encoding="utf-8")
    print(f"[verify] Report: {rob / f'{q.lower()}_robustness_report.md'}")
    print(f"[verify] Model: {args.model_type} | Checks: {len(req)}")

    if args.depth_check:
        text = args.depth_check
        if os.path.isfile(text):
            text = Path(text).read_text(encoding="utf-8")
        r = check_depth(text)
        st = "PASS" if r["passed"] else "FAIL"
        print(f"[verify] Depth: {r['level']} ({r['score']}/6) [{st}]")
        for i in r["issues"]:
            print(f"  - {i}")
        if not r["passed"]:
            print("[verify] BLOCKED: Model below L3 standard")

if __name__ == "__main__":
    main()

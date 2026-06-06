#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gate Contracts Module (KyrieZhang329-inspired)
===============================================
G1-G6 hard gate contracts with enter_condition / pass_criteria / fail_fallback.
Plus: P1 change propagation, G2 PoC enforcement, G4 frozen staleness, G6 enhanced audit.

Integrated into quality_gate.py for math-modeling-contest v5.6.0+.
"""

import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("CUMCM_Workspace")

# ═══════════════════════════════════════════════════════════════
# Gate Contracts
# ═══════════════════════════════════════════════════════════════

GATE_CONTRACTS = {
    "G1_PROBLEM_PARSED": {
        "description": "Problem parsed + classified + literature searched",
        "enter_condition": "User provides a problem statement (file or text).",
        "pass_criteria": [
            "Problem parsed into goals / objects / constraints / data / outputs / subquestions",
            "Each subquestion classified by task type (optimization / prediction / evaluation / hybrid)",
            "Related literature searched with >=2 refs per subquestion",
        ],
        "fail_fallback": "Route to problem analysis -> literature deep search. Do not advance to G2.",
    },
    "G2_METHOD_VALIDATED": {
        "description": "LOAD-BEARING: method->code boundary. Most failures happen here.",
        "enter_condition": "G1 passed; data preprocessed; workspace structured.",
        "pass_criteria": [
            "2-4 candidate methods per subquestion documented",
            "EVERY candidate has a <=30-line PoC script AND a small-scale feasibility result",
            "A candidate WITHOUT a PoC counts as 'not yet validated'",
        ],
        "fail_fallback": "Route to method selection -> PoC generation. Do not generate main code before G2 passes.",
    },
    "G3_CODE_REVIEWED": {
        "description": "Code review artifact on disk with >=5 explicit check items.",
        "enter_condition": "G2 passed; code generated for chosen methods.",
        "pass_criteria": [
            "Review artifact exists with >=5 explicit pass/fail items referencing file:line",
            "Verification report confirms correctness",
            "Numerical sanity check passed (no inf/nan/extreme values)",
        ],
        "fail_fallback": "Route to code reviewer. Do not advance experiments before G3 passes.",
    },
    "G4_RESULTS_FROZEN": {
        "description": "LOAD-BEARING: results->paper boundary. Prevents silent number drift.",
        "enter_condition": "G3 passed; experiments complete; robustness checked.",
        "pass_criteria": [
            "frozen_numbers.json exists for each subquestion",
            "Freeze is newer than ALL source files (no STALE freeze)",
            "freeze_change_log.md tracks all defrost events with reasons",
        ],
        "fail_fallback": "Follow thaw(log reason) -> modify(update source) -> re-freeze. Never edit frozen_numbers.json by hand.",
    },
    "G5_PAPER_SECTION_READY": {
        "description": "Paper section meets quality thresholds before final assembly.",
        "enter_condition": "G4 passed; paper sections drafted.",
        "pass_criteria": [
            "Section meets word-count floor",
            "Every numerical result discussed from >=3 dimensions",
            "Every figure passes render-check",
            "Model derivation depth >= L3",
        ],
        "fail_fallback": "Route to paper-section-writer -> figure-generator with missing-dimensions list.",
    },
    "G6_AUDIT_LAYER_PASSED": {
        "description": "FINAL GATE: 3 independent auditors ALL must PASS.",
        "enter_condition": "G5 passed for all subquestions; paper sections drafted; references managed.",
        "pass_criteria": [
            "Consistency audit PASSED with disk artifact",
            "Completeness audit PASSED with disk artifact",
            "Quality audit PASSED with disk artifact",
            "ALL THREE must PASS - one passing does not imply the others",
        ],
        "fail_fallback": "Route to whichever auditor failed. Never approve final_assembly_allowed=true on partial audit.",
    },
}


def print_gate_contracts():
    """Print all gate contracts for agent reference."""
    print("\n" + "=" * 70)
    print("  GATE CONTRACTS (KyrieZhang329-inspired)")
    print("=" * 70)
    for gate_id, contract in GATE_CONTRACTS.items():
        print(f"\n  [{gate_id}] {contract['description']}")
        print(f"    Enter:  {contract['enter_condition']}")
        for c in contract['pass_criteria']:
            print(f"    Pass:   - {c}")
        print(f"    Fail:   {contract['fail_fallback']}")
    print("\n" + "=" * 70)


# ═══════════════════════════════════════════════════════════════
# P1: Change Propagation Rule
# ═══════════════════════════════════════════════════════════════

def propagation_check(changed_files, workspace=None):
    """P1: Check what other files may be stale after changes.

    After modifying any file under code/, methods/, results/, or planning/:
      1. grep the entire workspace for references to the changed artifact
      2. List every file that may now be stale
      3. Either update it OR flag it as STALE with recommended repair

    Returns: dict with stale_files, frozen_affected, recommendations
    """
    if workspace is None:
        workspace = WORKSPACE

    identifiers = set()
    for cf in changed_files:
        cf_path = Path(cf)
        if cf_path.exists() and cf_path.suffix in ('.py', '.m', '.md', '.json'):
            try:
                text = cf_path.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            names = re.findall(r'\b([A-Za-z_][A-Za-z0-9_]{2,})\b', text)
            identifiers.update(names[:50])

    if not identifiers:
        return {"stale_files": [], "frozen_affected": [], "recommendations": []}

    stale_files = []
    frozen_affected = []
    search_dirs = ['methods', 'code', 'results', 'paper', 'planning']

    for search_dir in search_dirs:
        sd = workspace / search_dir
        if not sd.exists():
            continue
        for f in sd.rglob('*'):
            if not f.is_file() or f.suffix not in ('.py', '.m', '.md', '.tex', '.json'):
                continue
            if str(f) in [str(Path(cf)) for cf in changed_files]:
                continue
            try:
                text = f.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            matched = [ident for ident in identifiers if ident in text]
            if matched:
                rel = str(f.relative_to(workspace))
                stale_files.append({"file": rel, "matched_identifiers": matched[:10]})

    # Check frozen staleness
    for qdir in (workspace / 'frozen').glob('Q*') if (workspace / 'frozen').exists() else []:
        fp = qdir / 'frozen_numbers.json'
        if fp.exists():
            frozen_mtime = fp.stat().st_mtime
            for cf in changed_files:
                cf_path = Path(cf)
                if cf_path.exists() and cf_path.stat().st_mtime > frozen_mtime:
                    frozen_affected.append(str(qdir.name))
                    break

    recommendations = []
    if stale_files:
        recommendations.append(
            f"{len(stale_files)} files may be stale. Re-run consistency-auditor for affected subquestions."
        )
    if frozen_affected:
        recommendations.append(
            f"Frozen snapshots for {frozen_affected} are now STALE. "
            f"Follow unfreeze -> modify -> re-freeze protocol."
        )

    return {
        "stale_files": stale_files,
        "frozen_affected": frozen_affected,
        "recommendations": recommendations,
    }


def print_propagation_report(result):
    """Print P1 propagation check results."""
    print("\n" + "=" * 60)
    print("  P1: Change Propagation Check")
    print("=" * 60)

    if result["stale_files"]:
        print(f"\n  Potentially STALE files ({len(result['stale_files'])}):")
        for sf in result["stale_files"]:
            print(f"    - {sf['file']}")
            print(f"      matched: {', '.join(sf['matched_identifiers'][:5])}")
    else:
        print("\n  No stale files detected.")

    if result["frozen_affected"]:
        print(f"\n  STALE frozen snapshots: {result['frozen_affected']}")

    if result["recommendations"]:
        print("\n  Recommendations:")
        for rec in result["recommendations"]:
            print(f"    - {rec}")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════
# G2: PoC Hard Gate
# ═══════════════════════════════════════════════════════════════

def gate_g2_poc(poc_dir=None):
    """G2: Check every candidate method has a <=30-line PoC with feasibility result."""
    if poc_dir is None:
        methods_dir = WORKSPACE / "methods"
    else:
        methods_dir = Path(poc_dir)

    if not methods_dir.exists():
        return False, "G2 PoC: methods/ directory not found. Run method selection first.", {}

    poc_files = list(methods_dir.rglob("poc/*.py")) + list(methods_dir.rglob("poc/*.m"))

    if not poc_files:
        return False, (
            "G2 PoC FAILED: No PoC scripts found under methods/Qx/poc/.\n"
            "  Requirement: EVERY candidate method must have a <=30-line PoC with a feasibility result.\n"
            "  Candidates without PoC are NOT validated."
        ), {}

    issues = []
    validated = []
    for poc in poc_files:
        try:
            lines = poc.read_text(encoding='utf-8', errors='replace').split('\n')
        except Exception:
            issues.append(f"{poc.name}: cannot read")
            continue

        code_lines = [
            l for l in lines
            if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('%')
        ]
        line_count = len(code_lines)

        if line_count > 30:
            issues.append(f"{poc.name}: {line_count} code lines (max 30)")
        elif line_count == 0:
            issues.append(f"{poc.name}: empty PoC")
        else:
            text = '\n'.join(lines)
            has_output = any(kw in text for kw in ['print(', 'fprintf(', 'disp(', 'output', 'result'])
            if has_output:
                validated.append({"file": poc.name, "lines": line_count})
            else:
                issues.append(f"{poc.name}: no output/result statement found")

    if issues:
        return False, (
            f"G2 PoC FAILED: {len(issues)} issue(s).\n"
            + "\n".join(f"  - {i}" for i in issues) + "\n"
            f"  Validated: {len(validated)} PoC(s)."
        ), {"issues": issues, "validated": validated}

    return True, (
        f"G2 PoC PASSED: {len(validated)} candidate(s) validated.\n"
        + "\n".join(f"  - {v['file']}: {v['lines']} lines" for v in validated)
    ), {"validated": validated}


# ═══════════════════════════════════════════════════════════════
# G4: Frozen Staleness Detection
# ═══════════════════════════════════════════════════════════════

def gate_g4_frozen_staleness(subquestion=None):
    """G4: Check if frozen_numbers.json is stale (source files newer than freeze)."""
    frozen_root = WORKSPACE / "frozen"
    if not frozen_root.exists():
        return False, "G4: No frozen/ directory. Run freeze first.", {}

    subquestions = [subquestion] if subquestion else [
        d.name for d in frozen_root.iterdir() if d.is_dir()
    ]

    all_stale = []
    all_ok = []

    for q in subquestions:
        freeze_path = frozen_root / q / "frozen_numbers.json"
        if not freeze_path.exists():
            all_stale.append(f"{q}: no freeze exists")
            continue

        try:
            with open(freeze_path, 'r', encoding='utf-8') as f:
                frozen = json.load(f)
        except Exception:
            all_stale.append(f"{q}: corrupted freeze file")
            continue

        source_dir = Path(frozen.get("source_dir", ""))
        frozen_at = frozen.get("frozen_at", "unknown")
        frozen_dt = None
        try:
            frozen_dt = datetime.strptime(frozen_at, "%Y-%m-%d %H:%M:%S")
        except Exception:
            all_stale.append(f"{q}: unparseable frozen_at timestamp")
            continue

        newer_files = []
        if source_dir.exists():
            for fpath in source_dir.rglob("*"):
                if fpath.is_file() and fpath.suffix in ('.py', '.m', '.json', '.csv', '.txt', '.md'):
                    mtime = fpath.stat().st_mtime
                    if datetime.fromtimestamp(mtime) > frozen_dt:
                        newer_files.append(str(fpath.relative_to(source_dir)))

        if newer_files:
            frozen['status'] = 'stale'
            with open(freeze_path, 'w', encoding='utf-8') as f:
                json.dump(frozen, f, indent=2, ensure_ascii=False)
            all_stale.append(
                f"{q}: STALE (frozen {frozen_at}, {len(newer_files)} source files newer)"
            )
        else:
            all_ok.append(q)

    if all_stale:
        return False, (
            "G4 Frozen Staleness FAILED:\n"
            + "\n".join(f"  - {s}" for s in all_stale) + "\n"
            "  Action: thaw(log reason) -> modify(update source) -> re-freeze."
        ), {"stale": all_stale, "ok": all_ok}

    return True, f"G4 Frozen Staleness PASSED: {len(all_ok)} freeze(s) current.", {"ok": all_ok}


# ═══════════════════════════════════════════════════════════════
# G6: Enhanced Independent Audit Layer (with disk artifacts)
# ═══════════════════════════════════════════════════════════════

def _write_audit_artifact(ws, filename, verdict, evidence, issues, pass_criteria_key="G6_AUDIT_LAYER_PASSED"):
    """Write a disk audit artifact. Core principle: auditors MUST leave files."""
    audit_dir = ws / "paper" / "audits"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_path = audit_dir / filename

    lines = [f"# {filename.replace('.md', '').replace('_', ' ').title()}", "", f"**Verdict: {verdict}**", ""]
    lines.append("## Evidence")
    for e in evidence:
        lines.append(f"- [x] {e}")
    if issues:
        lines.append("")
        lines.append("## Issues")
        for i in issues:
            lines.append(f"- [ ] {i}")
    if pass_criteria_key in GATE_CONTRACTS:
        lines.append("")
        lines.append("## Pass Criteria")
        for pc in GATE_CONTRACTS[pass_criteria_key]["pass_criteria"]:
            lines.append(f"- {pc}")

    audit_path.write_text("\n".join(lines), encoding='utf-8')
    return str(audit_path)


def audit_consistency_enhanced(workspace_path):
    """G6 Layer 1: Cross-media consistency (paper <-> code <-> frozen_numbers.json)."""
    ws = Path(workspace_path)
    issues = []
    evidence = []

    paper_files = list(ws.glob("output/*.docx")) + list(ws.glob("output/*.pdf"))
    if not paper_files:
        issues.append("NO_PAPER: No output paper (.docx/.pdf) found")
    else:
        evidence.append(f"Paper: {paper_files[0].name} ({paper_files[0].stat().st_size} bytes)")

    frozen_files = list(ws.glob("frozen/*/frozen_numbers.json"))
    if not frozen_files:
        issues.append("NO_FROZEN: No frozen_numbers.json found - numbers may drift")
    else:
        for ff in frozen_files:
            try:
                with open(ff, 'r', encoding='utf-8') as f:
                    frozen = json.load(f)
                status = frozen.get('status', 'frozen')
                if status == 'stale':
                    issues.append(f"STALE_FREEZE: {ff.parent.name} freeze is stale")
                else:
                    evidence.append(f"Freeze {ff.parent.name}: {status} (v{frozen.get('version', '?')})")
            except Exception:
                issues.append(f"CORRUPT_FREEZE: {ff}")

    symbol_table = ws / "planning" / "symbol_table.md"
    if symbol_table.exists():
        evidence.append(f"Symbol table: {symbol_table.stat().st_size} bytes")
    else:
        issues.append("NO_SYMBOL_TABLE: planning/symbol_table.md not found")

    codemap = ws / "CODE_MAP.md"
    if codemap.exists():
        evidence.append(f"CODE_MAP: {codemap.stat().st_size} bytes")
    else:
        issues.append("NO_CODE_MAP: CODE_MAP.md not found")

    passed = len(issues) == 0
    artifact = _write_audit_artifact(ws, "cross_media_consistency_audit.md",
                                     "PASSED" if passed else "FAILED", evidence, issues)
    return {"passed": passed, "issues": issues, "evidence": evidence, "artifact": artifact}


def audit_completeness_enhanced(workspace_path):
    """G6 Layer 2: Completeness (every subquestion has code + results + report + robustness)."""
    ws = Path(workspace_path)
    issues = []
    evidence = []

    for q in ["Q1", "Q2", "Q3", "Q4"]:
        has_code = bool(list(ws.glob(f"code/{q}/*.py")) + list(ws.glob(f"code/{q}/*.m")))
        has_results = bool(list(ws.glob(f"results/{q}/**/*")))
        has_robustness = (ws / f"robustness/{q}").exists()

        if not has_code and not has_results:
            continue

        parts = []
        if has_code:
            parts.append("code")
        else:
            issues.append(f"{q}: no code found")
        if has_results:
            parts.append("results")
        else:
            issues.append(f"{q}: no results found")
        if has_robustness:
            parts.append("robustness")
        else:
            issues.append(f"{q}: no robustness report")
        if parts:
            evidence.append(f"{q}: {' + '.join(parts)}")

    passed = len(issues) == 0
    artifact = _write_audit_artifact(ws, "completeness_audit.md",
                                     "PASSED" if passed else "FAILED", evidence, issues)
    return {"passed": passed, "issues": issues, "evidence": evidence, "artifact": artifact}


def audit_quality_enhanced(workspace_path):
    """G6 Layer 3: Quality (anti-fabrication, academic integrity, paper quality)."""
    ws = Path(workspace_path)
    issues = []
    evidence = []

    frozen_files = list(ws.glob("frozen/*/frozen_numbers.json"))
    if frozen_files:
        evidence.append(f"{len(frozen_files)} frozen snapshot(s) - numbers traceable")
    else:
        issues.append("UNTRACEABLE: No frozen numbers - cannot verify numbers trace to code")

    integrity_log = ws / "integrity_gate.md"
    if integrity_log.exists():
        evidence.append("Integrity gate log found")
    else:
        issues.append("NO_INTEGRITY_CHECK: integrity gate not run")

    for docx in ws.glob("output/*.docx"):
        size_kb = docx.stat().st_size / 1024
        if size_kb < 30:
            issues.append(f"SMALL_PAPER: {docx.name} is only {size_kb:.0f}KB - likely incomplete")
        else:
            evidence.append(f"Paper size: {size_kb:.0f}KB")

    codemap = ws / "CODE_MAP.md"
    if codemap.exists():
        text = codemap.read_text(encoding='utf-8', errors='replace')
        if len(text) < 500:
            issues.append("THIN_CODE_MAP: Model documentation too brief")
        else:
            evidence.append(f"CODE_MAP: {len(text)} chars")

    passed = len(issues) == 0
    artifact = _write_audit_artifact(ws, "qa_report.md",
                                     "PASSED" if passed else "FAILED", evidence, issues)
    return {"passed": passed, "issues": issues, "evidence": evidence, "artifact": artifact}


def run_g6_audit_enhanced(workspace_path=None):
    """Run full G6 three-layer audit with disk artifacts. ALL THREE must PASS."""
    if workspace_path is None:
        workspace_path = str(WORKSPACE)

    ws = Path(workspace_path)

    results = {
        "consistency": audit_consistency_enhanced(workspace_path),
        "completeness": audit_completeness_enhanced(workspace_path),
        "quality": audit_quality_enhanced(workspace_path),
    }

    all_passed = all(r["passed"] for r in results.values())
    results["gate_passed"] = all_passed

    # Write final assembly gate status
    gate_file = ws / "paper" / "gate_g6_status.json"
    gate_file.parent.mkdir(parents=True, exist_ok=True)
    gate_file.write_text(json.dumps({
        "gate": "G6_AUDIT_LAYER_PASSED",
        "passed": all_passed,
        "final_assembly_allowed": all_passed,
        "auditors": {
            k: {"passed": v["passed"], "artifact": v.get("artifact", "N/A")}
            for k, v in results.items() if k != "gate_passed"
        },
    }, indent=2, ensure_ascii=False), encoding='utf-8')

    return results


def print_g6_enhanced_report(results):
    """Print enhanced G6 audit report."""
    print("\n" + "=" * 60)
    print("  G6 Audit Layer (Consistency -> Completeness -> Quality)")
    print("  ALL THREE must PASS - one passing != others passing")
    print("=" * 60)

    icons = {True: "PASS", False: "FAIL"}
    for layer, r in results.items():
        if layer == "gate_passed":
            continue
        icon = icons[r["passed"]]
        print(f"\n  [{icon}] {layer.upper()}")
        for e in r.get("evidence", []):
            print(f"    + {e}")
        for issue in r.get("issues", []):
            print(f"    - {issue}")
        if "artifact" in r:
            print(f"    artifact: {r['artifact']}")

    gate_icon = "PASS" if results["gate_passed"] else "BLOCKED"
    print(f"\n  G6 GATE: [{gate_icon}]")
    if not results["gate_passed"]:
        print("  Pipeline blocked until all three auditors PASS.")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════
# CLI entry point (when run directly)
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Gate Contracts & Enhanced Audits")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("contracts", help="Print all gate contracts")
    sp = sub.add_parser("poc", help="Run G2 PoC gate")
    sp.add_argument("--poc-dir", default=None)

    sp = sub.add_parser("stale", help="Run G4 frozen staleness check")
    sp.add_argument("--subquestion", "-q", default=None)

    sp = sub.add_parser("g6", help="Run G6 enhanced three-layer audit")
    sp.add_argument("--workspace", "-w", default=None)

    sp = sub.add_parser("propagate", help="Run P1 change propagation check")
    sp.add_argument("--changed", "-c", nargs="+", required=True)

    args = p.parse_args()

    if args.cmd == "contracts":
        print_gate_contracts()
    elif args.cmd == "poc":
        passed, msg, details = gate_g2_poc(args.poc_dir)
        print(f"{'PASS' if passed else 'FAIL'}: {msg}")
        sys.exit(0 if passed else 1)
    elif args.cmd == "stale":
        passed, msg, details = gate_g4_frozen_staleness(args.subquestion)
        print(f"{'PASS' if passed else 'FAIL'}: {msg}")
        sys.exit(0 if passed else 1)
    elif args.cmd == "g6":
        results = run_g6_audit_enhanced(args.workspace)
        print_g6_enhanced_report(results)
        sys.exit(0 if results["gate_passed"] else 1)
    elif args.cmd == "propagate":
        result = propagation_check(args.changed)
        print_propagation_report(result)
    else:
        p.print_help()

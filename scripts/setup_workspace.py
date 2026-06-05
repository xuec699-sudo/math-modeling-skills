#!/usr/bin/env python3
"""
Math Modeling Contest - Workspace Setup
Creates standardized contest workspace structure.

Usage:
  python scripts/setup_workspace.py                  # CUMCM (国赛) mode
  python scripts/setup_workspace.py --mode mcm       # MCM/ICM (美赛) mode
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

ROOT = Path("CUMCM_Workspace")

DIRS = [
    ROOT / "data",
    ROOT / "src" / "models",
    ROOT / "src" / "verifications",
    ROOT / "latex" / "images",
    ROOT / "memory",
    ROOT / "state",
    ROOT / "output",
]

PENDING_CUMCM = [
    "Phase 1: Problem analysis & literature research",
    "Phase 2: Data preprocessing (EDA)",
    "Phase 3: Model building & verification (per sub-problem)",
    "Phase 4: Sensitivity analysis",
    "Phase 5: LaTeX paper writing (Chinese)",
    "Phase 6: PDF compilation",
]

PENDING_MCM = [
    "Phase 1: Problem analysis & literature research",
    "Phase 2: Data preprocessing (EDA)",
    "Phase 3: Model building & verification (per sub-problem)",
    "Phase 4: Sensitivity analysis",
    "Phase 5: Summary page + full paper LaTeX (English)",
    "Phase 6: Memo/letter (if required)",
    "Phase 7: PDF compilation",
]


def setup(mode: str = "cumcm"):
    is_mcm = mode.lower() == "mcm"
    label = "MCM/ICM" if is_mcm else "CUMCM"

    print("=" * 58)
    print(f"  {label} Math Modeling Contest - Workspace Setup")
    if is_mcm:
        print("  Mode: MCM/ICM (English paper, mcmthesis)")
    else:
        print("  Mode: CUMCM (Chinese paper)")
    print("=" * 58)

    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  [create] {d}")

    # iteration.json
    iteration_file = ROOT / "memory" / "iteration.json"
    if not iteration_file.exists():
        state = {
            "title": "",
            "mode": mode.lower(),
            "phase": "init",
            "phase_index": 0,
            "problems": [],
            "models": [],
            "iterations": 0,
            "contest_type": "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_tasks": [],
            "pending_tasks": PENDING_MCM if is_mcm else PENDING_CUMCM,
        }
        iteration_file.write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  [create] {iteration_file}")

    # LaTeX template
    if is_mcm:
        template_src = SKILL_ROOT / "templates" / "mcm_template.tex"
        template_dst = ROOT / "latex" / "main.tex"
        if template_src.exists() and not template_dst.exists():
            shutil.copy(template_src, template_dst)
            print(f"  [copy] MCM template -> {template_dst}")
        elif not template_dst.exists():
            print(f"  [warn] Template {template_src} not found, place manually")
            template_dst.write_text("% MCM/ICM Paper Template\n", encoding="utf-8")
    else:
        template_src = SKILL_ROOT / "templates" / "cumcm_template.tex"
        template_dst = ROOT / "latex" / "main.tex"
        if template_src.exists() and not template_dst.exists():
            shutil.copy(template_src, template_dst)
            print(f"  [copy] CUMCM template -> {template_dst}")
        elif not template_dst.exists():
            print(f"  [warn] Template {template_src} not found, place manually")
            template_dst.write_text("% CUMCM Paper Template\n", encoding="utf-8")

    # Memory files
    thought_file = ROOT / "memory" / "thought_process.md"
    if not thought_file.exists():
        header = "# Thought Process Log\n\n" if is_mcm else "# 思考过程记录\n\n"
        thought_file.write_text(
            header + "> Workspace initialized. Awaiting problem input.\n",
            encoding="utf-8"
        )
        print(f"  [create] {thought_file}")

    eval_file = ROOT / "memory" / "evaluation_log.md"
    if not eval_file.exists():
        header = "# Feedback & Evaluation Log\n\n" if is_mcm else "# 用户反馈评价记录\n\n"
        eval_file.write_text(header + "(No feedback yet)\n", encoding="utf-8")
        print(f"  [create] {eval_file}")

    # src/__init__.py
    init_py = ROOT / "src" / "__init__.py"
    if not init_py.exists():
        init_py.write_text("# Math modeling source package\n", encoding="utf-8")

    print()
    print(f"  Workspace ready! Mode: {'MCM/ICM (English)' if is_mcm else 'CUMCM (Chinese)'}")
    print(f"  Directory: {ROOT.resolve()}")
    print("=" * 58)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["cumcm", "mcm"], default="cumcm",
                        help="Contest mode: cumcm (国赛) or mcm (美赛)")
    args = parser.parse_args()
    setup(mode=args.mode)

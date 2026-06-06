#!/usr/bin/env python3
"""
Math Modeling Contest - Workspace Setup (v2)
Creates isolated contest workspace per contest under contests/

Usage:
  python scripts/setup_workspace.py --name "APMCM2025_A_农业灌溉"
  python scripts/setup_workspace.py --name "MCM2026_B" --mode mcm
"""

import argparse, json, shutil, sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

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


def setup(name: str, mode: str = "cumcm", base_dir: Path = None):
    if not name:
        print("[ERROR] --name is required.")
        sys.exit(1)

    if base_dir is None:
        base_dir = Path("contests")

    contest_root = base_dir / name
    is_mcm = mode.lower() == "mcm"
    label = "MCM/ICM" if is_mcm else "CUMCM/APMCM"

    DIRS = [
        contest_root / "data",
        contest_root / "src" / "models",
        contest_root / "src" / "verifications",
        contest_root / "latex" / "images",
        contest_root / "memory",
        contest_root / "state",
        contest_root / "output",
        contest_root / "output" / "figures",
        contest_root / "output" / "images",
    ]

    print("=" * 60)
    print(f"  {label} Workspace: {name}")
    print("=" * 60)

    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  [create] {d}")

    # iteration.json
    iteration_file = contest_root / "memory" / "iteration.json"
    if not iteration_file.exists():
        state = {
            "contest_name": name,
            "title": "",
            "mode": mode.lower(),
            "phase": "init",
            "phase_index": 0,
            "problems": [],
            "models": [],
            "iterations": 0,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_tasks": [],
            "pending_tasks": PENDING_MCM if is_mcm else PENDING_CUMCM,
        }
        iteration_file.write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  [create] memory/iteration.json")

    # README
    readme = contest_root / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {name}\n\n"
            f"- Contest: {name}\n"
            f"- Mode: {mode}\n"
            f"- Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"## 目录\n\n"
            f"| 目录 | 用途 |\n|------|------|\n"
            f"| `data/` | 赛题数据 |\n"
            f"| `src/` | 模型代码 |\n"
            f"| `latex/` | LaTeX 源码 |\n"
            f"| `output/` | 论文输出 (DOCX/PDF) |\n"
            f"| `output/figures/` | 图表 |\n"
            f"| `output/images/` | 插图 |\n"
            f"| `memory/` | 思考记录 |\n"
            f"| `state/` | 流水线状态 |\n",
            encoding="utf-8"
        )
        print(f"  [create] README.md")

    # LaTeX template
    template_src = (
        SKILL_ROOT / "templates" / "mcm_template.tex" if is_mcm
        else SKILL_ROOT / "templates" / "cumcm_template.tex"
    )
    template_dst = contest_root / "latex" / "main.tex"
    if template_src.exists() and not template_dst.exists():
        shutil.copy(template_src, template_dst)
        print(f"  [copy] {template_src.name} -> latex/main.tex")

    # Init files
    (contest_root / "memory" / "thought_process.md").write_text(
        "# 思考过程记录\n\n> Workspace initialized.\n", encoding="utf-8"
    )
    (contest_root / "memory" / "evaluation_log.md").write_text(
        "# 评价记录\n\n(暂无)\n", encoding="utf-8"
    )
    (contest_root / "src" / "__init__.py").write_text(
        "# Math modeling source\n", encoding="utf-8"
    )

    # Copy EDA template
    eda_src = SKILL_ROOT / "templates" / "eda_template.py"
    eda_dst = contest_root / "src" / "eda_preprocess.py"
    if eda_src.exists():
        shutil.copy(eda_src, eda_dst)
        print(f"  [copy] eda_template.py -> src/eda_preprocess.py")

    print()
    print(f"  Workspace ready: {contest_root.resolve()}")
    print(f"  Put contest data in: {contest_root / 'data'}")
    print(f"  Start EDA: python src/eda_preprocess.py")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup contest workspace")
    parser.add_argument("--name", required=True, help="Contest name")
    parser.add_argument("--mode", choices=["cumcm", "mcm"], default="cumcm")
    parser.add_argument("--root", default="contests", help="Base directory")
    args = parser.parse_args()
    setup(name=args.name, mode=args.mode, base_dir=Path(args.root))

#!/usr/bin/env python3
"""
Math Modeling Contest — Submission Package Generator
=====================================================
Generates a ready-to-submit ZIP with paper + code + data + CODE_MAP.

Usage:
  python scripts/make_submission.py --name "APMCM2025_A_农业灌溉"
  python scripts/make_submission.py --name "51MCM2026_A" --output ./提交
  python scripts/make_submission.py --all  # package all contests
"""

import argparse, os, shutil, sys, zipfile
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONTESTS = Path("contests")


def make_submission(workspace: Path, output_dir: Path = None):
    """Generate submission zip for a contest workspace"""
    name = workspace.name
    if output_dir is None:
        output_dir = Path("submissions")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{name}_提交包_{timestamp}.zip"
    zip_path = output_dir / zip_name

    # Files to include
    included = []
    excluded = []

    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(str(workspace)):
            # Skip empty dirs and archives
            dirs[:] = [d for d in dirs if d not in ("_archive", "__pycache__", ".git")]

            for fname in files:
                fpath = Path(root) / fname
                rel = fpath.relative_to(workspace.parent)

                # Skip: compile artifacts, empty templates, temp files
                if fname.endswith((".aux", ".log", ".toc", ".synctex.gz", ".out", ".pyc")):
                    excluded.append(str(rel))
                    continue
                if fname in ("iteration.json", "thought_process.md", "evaluation_log.md"):
                    # Only include if they have real content
                    try:
                        text = fpath.read_text(encoding="utf-8")
                        if len(text.strip()) < 60:
                            excluded.append(str(rel))
                            continue
                    except:
                        excluded.append(str(rel))
                        continue

                zf.write(str(fpath), str(rel))
                included.append(str(rel))

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\n{'='*60}")
    print(f"  Submission: {name}")
    print(f"  ZIP: {zip_path}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Files: {len(included)} included, {len(excluded)} skipped")
    print(f"{'='*60}")

    # Print summary
    print(f"\n  Contents:")
    for f in sorted(included):
        print(f"    {f}")

    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Generate submission packages")
    parser.add_argument("--name", help="Contest name to package")
    parser.add_argument("--all", action="store_true", help="Package ALL contests")
    parser.add_argument("--root", default=str(DEFAULT_CONTESTS), help="Contests directory")
    parser.add_argument("--output", default="submissions", help="Output directory")
    args = parser.parse_args()

    base = Path(args.root)
    if not base.exists():
        sys.exit(f"[ERROR] Not found: {base}")

    output = Path(args.output)

    if args.all:
        for ws in sorted(base.iterdir()):
            if ws.is_dir() and not ws.name.startswith("."):
                make_submission(ws, output)
    elif args.name:
        ws = base / args.name
        if not ws.exists():
            sys.exit(f"[ERROR] Contest not found: {ws}")
        make_submission(ws, output)
    else:
        parser.print_help()

    print(f"\nAll submissions saved to: {output.resolve()}")


if __name__ == "__main__":
    main()

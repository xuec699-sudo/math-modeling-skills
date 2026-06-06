#!/usr/bin/env python3
"""
Math Modeling Contest — Smart Workspace Cleanup (v2)
=====================================================
KEEPS: solving code, data, final papers, figures
DELETES: compile artifacts, intermediate drafts, paper-gen scripts

Usage:
  python scripts/cleanup_workspace.py --name "CUMCM2025_B"
  python scripts/cleanup_workspace.py --all --dry-run
"""

import argparse, os, shutil, sys, re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# === DELETE RULES ===

# 1. Compile artifacts (always safe to delete)
COMPILE_EXT = {".aux", ".log", ".toc", ".synctex.gz", ".out", ".bbl", ".blg", ".run.xml"}

# 2. DOCX generation scripts (NOT solving code — these just build the DOCX)
DOCGEN_SCRIPTS = {
    "build_paper.py", "gen_final_paper.py", "generate_paper.py",
    "gen_final_paper.py", "paper_body1.py", "paper_final.py",
    "paper_final_v2.py", "paper_v3.py", "paper_v4.py",
    "append_body.py", "fix_paper.py", "writer.py",
    "render_formulas.py", "gen_docx.py", "gen_final_docx.py",
    "generate_docx.py", "post_process.py", "post_process_v2.py",
    "post_process_v3.py", "post_process_v4.py",
    "write_expanded_paper.py", "p1_encrypt.py", "p2_assignment.py",
    "p3_p4_p5.py", "p6_application.py",
}

# 3. Test files
TEST_FILES = {"test_minimal.docx", "test_omml_v2.docx", "test_omml_v3.docx",
              "_test_fig.docx", "test_build_output.docx",
              "test_omml_min.py", "test_omml_v2_run.py", "test_omml_v3.py",
              "test_math.py", "test_math2.py", "test_math2.docx",
              "test_cn.py", "test_chinese_search.py", "test_eq.png"}

# 4. Intermediate versions (keep only "final" or "最终" versions)
INTERMEDIATE_DOCX = re.compile(
    r"paper_(v[2-9]|step\d|final_v[23]|C_v[23]|C_final(?!_2026))\w*\.docx$|"
    r"paper_final(?!_2026)\.docx$|"
    r"paper_final_pandoc\.docx$"
)

# 5. Intermediate text/JSON dumps
TEMP_DUMPS = {
    "paper_text.txt", "paper_v2_text.txt", "paper_optimized_text.txt",
    "paper_review.txt", "paper_paras.json", "paper_tables.json",
    "paper_structure.json", "problem_paras.json", "results.json",
    "c_problem_results.json", "final_results.json", "paper_content.json",
    "unicode_analysis.json", "SOLUTION_REPORT.md",
}

# 6. Generic/unrelated images
GENERIC_IMAGES = {
    "demo.png", "demo-2.png", "test_eq.png",
    "image1.png", "image2.png", "image3.png",
    "image4.png", "image5.png", "image6.png",
    "wordcloud_all.png", "wordcloud_bad.png", "wordcloud_good.png",
    "rating_dist.png", "sentiment_pie.png",
}

# 7. Draft markdown (keep only if it's the sole paper source)
DRAFT_MD = {"draft.md", "draft_v2.md", "draft_paper_v2.md"}

# 8. Empty/template files to delete
EMPTY_TEMPLATES = {
    "src/__init__.py",
    "memory/evaluation_log.md", "memory/thought_process.md",
    "memory/iteration.json",
}

# === Files to ALWAYS KEEP (never delete) ===
ALWAYS_KEEP = {"README.md", "main.tex"}


def is_core_code(filename: str) -> bool:
    """Is this a core solving script (not paper generation)?"""
    name = Path(filename).name.lower()
    # Core solving indicators
    if any(kw in name for kw in ["solve", "model", "algorithm", "final_", "_final"]):
        return True
    if name in DOCGEN_SCRIPTS or name in TEST_FILES:
        return False
    # .py files that are not docgen/test are likely core code
    if name.endswith(".py"):
        return True
    return False


def should_delete(filepath: Path, workspace_root: Path) -> tuple[bool, str]:
    """Decide if a file should be deleted. Returns (delete, reason)."""
    name = filepath.name
    rel = str(filepath.relative_to(workspace_root))

    # Never delete these
    if name in ALWAYS_KEEP:
        return False, "protected"

    # Don't touch data directory
    if rel.startswith("data" + os.sep) or rel == "data":
        return False, "data"

    # 1. Compile artifacts
    if filepath.suffix in COMPILE_EXT:
        return True, "compile artifact"

    # 2. DOCX generation scripts
    if name in DOCGEN_SCRIPTS:
        return True, "docgen script"

    # 3. Test files
    if name in TEST_FILES:
        return True, "test file"

    # 4. Intermediate DOCX versions
    if INTERMEDIATE_DOCX.search(name):
        return True, "intermediate version"

    # 5. Temp dumps
    if name in TEMP_DUMPS:
        return True, "temp dump"

    # 6. Generic images
    if name in GENERIC_IMAGES:
        return True, "generic image"

    # 7. Draft markdown
    if name in DRAFT_MD:
        return True, "draft markdown"

    # 8. Empty templates
    if rel.replace("\\", "/") in EMPTY_TEMPLATES:
        try:
            text = filepath.read_text(encoding="utf-8").strip()
            if len(text) < 60:
                return True, "empty template"
        except:
            pass

    # 9. Python cache
    if "__pycache__" in rel:
        return True, "pycache"

    return False, "keep"


def cleanup_workspace(workspace: Path, dry_run: bool = False):
    """Clean a single workspace"""
    name = workspace.name
    deleted = 0
    freed = 0

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Cleaning: {name}")

    for f in sorted(workspace.rglob("*"), reverse=True):
        if f.is_file():
            do_delete, reason = should_delete(f, workspace)
            if do_delete:
                if dry_run:
                    rel = f.relative_to(workspace)
                    print(f"  would del [{reason}]: {rel}")
                else:
                    try:
                        size = f.stat().st_size
                        os.remove(str(f))
                        freed += size
                        deleted += 1
                        rel = f.relative_to(workspace)
                        print(f"  DEL [{reason}]: {rel}")
                    except Exception as e:
                        print(f"  ERR: {f.name} - {e}")
        elif f.is_dir() and not dry_run:
            # Remove empty directories
            try:
                if not any(f.iterdir()):
                    f.rmdir()
            except:
                pass

    if not dry_run:
        print(f"  → {deleted} files removed, {freed/1024:.0f} KB freed")
    elif deleted == 0:
        print("  (nothing to clean)")


def main():
    parser = argparse.ArgumentParser(description="Smart contest workspace cleanup")
    parser.add_argument("--name", help="Clean specific contest")
    parser.add_argument("--all", action="store_true", help="Clean ALL workspaces")
    parser.add_argument("--root", default="contests", help="Base directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    base = Path(args.root)
    if not base.exists():
        sys.exit(f"[ERROR] Not found: {base}")

    if args.all:
        for ws in sorted(base.iterdir()):
            if ws.is_dir() and not ws.name.startswith("."):
                cleanup_workspace(ws, args.dry_run)
    elif args.name:
        ws = base / args.name
        if not ws.exists():
            sys.exit(f"[ERROR] Not found: {ws}")
        cleanup_workspace(ws, args.dry_run)
    else:
        parser.print_help()

    print(f"\n{'[DRY RUN — no files deleted]' if args.dry_run else 'Done!'}")


if __name__ == "__main__":
    main()

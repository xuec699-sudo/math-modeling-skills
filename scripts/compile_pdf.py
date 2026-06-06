#!/usr/bin/env python3
"""
Math Modeling Contest - LaTeX to PDF Compiler

Detects available LaTeX engine (xelatex > pdflatex) and compiles the paper.
Supports both CUMCM (Chinese) and MCM/ICM (English) templates.

Usage:
  python scripts/compile_pdf.py                    # Compile CUMCM_Workspace/latex/main.tex
  python scripts/compile_pdf.py --main FILE        # Compile specific file
  python scripts/compile_pdf.py --engine xelatex   # Force specific engine
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = Path("CUMCM_Workspace")
DEFAULT_MAIN = WORKSPACE / "latex" / "main.tex"


def find_latex_engine() -> str:
    """Find available LaTeX engine. Prefer xelatex for Unicode support."""
    # Known good engine paths (verified on this system)
    KNOWN_PATHS = [
        r"C:\Users\CX\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe",
    ]
    for path in KNOWN_PATHS:
        if os.path.exists(path):
            return path
    for engine in ["xelatex", "pdflatex", "lualatex"]:
        if shutil.which(engine):
            return engine
    return ""


def compile_pdf(main_file: str, engine: str = "", bibtex: bool = False) -> bool:
    """Compile LaTeX to PDF. Returns True on success."""
    main_path = Path(main_file).resolve()
    if not main_path.exists():
        print(f"[compile] ERROR: File not found: {main_path}")
        return False

    tex_dir = main_path.parent
    tex_name = main_path.stem

    if not engine:
        engine = find_latex_engine()
        if not engine:
            print("[compile] ERROR: No LaTeX engine found.")
            print("  Install TeX Live (https://tug.org/texlive/) or MiKTeX (https://miktex.org/)")
            return False

    print(f"[compile] Using engine: {engine}")
    print(f"[compile] Source: {main_path}")

    # Run LaTeX twice for proper cross-references
    for run in range(1, 3):
        print(f"[compile] Pass {run}/2...")

        # Use -interaction=nonstopmode to prevent interactive prompts
        result = subprocess.run(
            [engine,
             "-synctex=1",
             "-interaction=nonstopmode",
             "-file-line-error",
             "-output-directory", str(tex_dir),
             str(main_path)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(tex_dir),
        )

        if result.returncode != 0:
            # Extract error summary
            errors = []
            for line in result.stdout.split("\n") + result.stderr.split("\n"):
                if line.startswith("!"):
                    errors.append(line.strip())
            if errors:
                print(f"[compile] Errors in pass {run}:")
                for e in errors[:10]:
                    print(f"  {e}")
            print(f"[compile] Full log: {tex_dir}/{tex_name}.log")
            return False

        print(f"[compile] Pass {run} OK")

    # Copy PDF to output directory
    pdf_src = tex_dir / f"{tex_name}.pdf"
    if pdf_src.exists():
        output_dir = WORKSPACE / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_dst = output_dir / f"{tex_name}.pdf"
        shutil.copy(pdf_src, pdf_dst)
        print(f"[compile] SUCCESS: PDF -> {pdf_dst}")
        print(f"[compile] Size: {pdf_dst.stat().st_size / 1024:.1f} KB")

        # Auto-cleanup compile artifacts
        for ext in [".aux", ".log", ".toc", ".synctex.gz", ".out"]:
            artifact = tex_dir / f"{tex_name}{ext}"
            if artifact.exists():
                try:
                    os.remove(str(artifact))
                except:
                    pass

        return True
    else:
        print(f"[compile] ERROR: PDF not generated at {pdf_src}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Compile LaTeX to PDF for math modeling contest")
    parser.add_argument("--main", default=str(DEFAULT_MAIN),
                        help=f"Path to main .tex file (default: {DEFAULT_MAIN})")
    parser.add_argument("--engine", default="",
                        help="LaTeX engine (xelatex, pdflatex, lualatex). Auto-detected if omitted.")
    args = parser.parse_args()

    success = compile_pdf(args.main, args.engine)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

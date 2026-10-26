#!/usr/bin/env python3
"""Free Car Care Pack — build script.

Renders every HTML sheet in src/ to a print-ready PDF in printables/
using WeasyPrint. Entirely local: no accounts, no network, no secrets.

Usage:
    python3 build.py                 # build all sheets
    python3 build.py --clean         # delete printables/*.pdf first
    python3 build.py --only glovbox  # build sheets whose name matches a substring

Each PDF starts with a friendly "getting started" page, then the
printable sheet pages. Print at 100% scale on US Letter.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "printables"


def clean() -> int:
    removed = 0
    if OUT.exists():
        for pdf in sorted(OUT.glob("*.pdf")):
            pdf.unlink()
            removed += 1
    print(f"Cleaned {removed} PDF(s) from {OUT}")
    return 0


def build(only: str | None = None) -> int:
    sheets = sorted(SRC.glob("*.html"))
    if only:
        sheets = [s for s in sheets if only.lower() in s.name.lower()]
        if not sheets:
            print(f"No sheet matched --only {only!r}", file=sys.stderr)
            return 1
    if not sheets:
        print(f"No .html sheets found in {SRC}", file=sys.stderr)
        return 1

    OUT.mkdir(exist_ok=True)

    failures = 0
    for sheet in sheets:
        dest = OUT / f"{sheet.stem}.pdf"
        try:
            HTML(filename=str(sheet), base_url=str(SRC)).write_pdf(str(dest))
            size_kb = dest.stat().st_size / 1024
            print(f"Built {dest.name:36s} {size_kb:7.1f} KB")
        except Exception as exc:  # keep building the rest, report at the end
            failures += 1
            print(f"FAILED {sheet.name}: {exc}", file=sys.stderr)

    if failures:
        print(f"\n{failures} sheet(s) failed to build.", file=sys.stderr)
        return 1
    print(f"\nDone. {len(sheets)} PDF(s) ready in {OUT}/")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build print-ready PDFs from the HTML sheets in src/."
    )
    parser.add_argument(
        "--clean", action="store_true", help="delete printables/*.pdf and exit"
    )
    parser.add_argument(
        "--only", metavar="NAME", help="build only sheets whose filename contains NAME"
    )
    args = parser.parse_args()

    if args.clean:
        return clean()
    return build(args.only)


if __name__ == "__main__":
    raise SystemExit(main())

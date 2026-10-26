"""Tests for the Free Car Care Pack.

Verifies that every sheet in src/ builds a valid PDF into printables/,
beyond just "the command didn't crash": we re-render each sheet in a
temp directory and also validate the committed outputs with pypdf.

Run with:  python3 -m pytest tests/ -q
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
PRINTABLES = ROOT / "printables"

SHEETS = sorted(SRC.glob("*.html"))

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)


def sheet_title(sheet: Path) -> str:
    match = TITLE_RE.search(sheet.read_text(encoding="utf-8"))
    assert match, f"{sheet.name} is missing a <title> tag"
    return match.group(1)


def render_to(tmp_path: Path, sheet: Path) -> bytes:
    """Render a sheet in isolation (tmp dir) and return the PDF bytes."""
    import shutil

    workdir = tmp_path / sheet.stem
    workdir.mkdir(exist_ok=True)
    shutil.copy(sheet, workdir / sheet.name)
    shutil.copy(SRC / "base.css", workdir / "base.css")
    dest = workdir / "out.pdf"
    HTML(filename=str(sheet), base_url=str(SRC)).write_pdf(str(dest))
    return dest.read_bytes()


@pytest.mark.parametrize("sheet", SHEETS, ids=lambda p: p.name)
def test_sheet_renders_valid_pdf(sheet: Path, tmp_path: Path):
    data = render_to(tmp_path, sheet)
    # Real PDFs start with a %PDF- header
    assert data[:5] == b"%PDF-", f"{sheet.name} did not produce a PDF header"

    reader = PdfReader(__import__("io").BytesIO(data))
    # Every sheet needs at least an intro page and the printable sheet page(s)
    assert len(reader.pages) >= 2, f"{sheet.name} rendered too few pages"


@pytest.mark.parametrize("sheet", SHEETS, ids=lambda p: p.name)
def test_pdf_text_contains_title(sheet: Path, tmp_path: Path):
    import html as html_mod
    import io

    # Unescape entities (&amp;) and drop ALL spaces: PDF text extraction can
    # inject kerning spaces ("T een-Driver") that aren't really there.
    title = html_mod.unescape(sheet_title(sheet))
    want = "".join(title.split()).lower()

    data = render_to(tmp_path, sheet)
    reader = PdfReader(io.BytesIO(data))
    first_page_text = reader.pages[0].extract_text() or ""
    got = "".join(first_page_text.split()).lower()
    assert want in got


@pytest.mark.parametrize("sheet", SHEETS, ids=lambda p: p.name)
def test_sheet_carries_manual_reminder(sheet: Path):
    html = sheet.read_text(encoding="utf-8")
    assert "Verify with your manual" in html, (
        f"{sheet.name} must include a 'Verify with your manual' reminder"
    )
    assert 'class="intro"' in html, (
        f"{sheet.name} must include a kind getting-started intro page"
    )


def test_build_script_produces_all_pdfs():
    """Runs the actual build script; this doubles as documentation that
    `python3 build.py` is the one command you need."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py")],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, f"build.py failed:\n{result.stdout}\n{result.stderr}"

    expected = {sheet.stem for sheet in SHEETS}
    produced = {pdf.stem for pdf in PRINTABLES.glob("*.pdf")}
    assert expected <= produced, f"missing PDFs: {expected - produced}"

    for pdf_path in sorted(PRINTABLES.glob("*.pdf")):
        assert pdf_path.read_bytes()[:5] == b"%PDF-", f"{pdf_path.name} is not a valid PDF"
        reader = PdfReader(str(pdf_path))
        assert len(reader.pages) >= 2, f"{pdf_path.name} has too few pages"

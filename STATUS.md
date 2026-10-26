# STATUS.md — Free Car Care Pack

Date: 2026-10-26
Status: complete and verified

## What was built

Seven family-car printable packets, each an unbranded PDF that opens with a
kind "getting started" page (page 1) followed by the printable sheet itself.
Every sheet includes a built-in "Verify with your manual" reminder, since
intervals, pressures, jack points, and state laws differ by model and state.

1. `maintenance-schedule.pdf` — fill-in service intervals copied from the
   owner's manual for *your* model, plus tire PSI, shop info, odometer log.
2. `service-visit-log.pdf` — one row per visit: date, odometer, shop, work,
   cost, where the receipt lives, work-warranty notes, running total.
3. `glovebox-info-card.pdf` — car/insurance/emergency numbers, breakdown
   steps, and a fender-bender photo/swap/call checklist.
4. `winter-car-kit.pdf` — trunk-kit checklist (★ = budget basics) plus a
   one-evening get-winter-ready list.
5. `road-trip-day-of-checks.pdf` — week-before prep page and a 15-minute
   departure-morning walk-around, with a trip-info card for the contact at
   home.
6. `used-car-checklist.pdf` — pre-purchase look-over and test-drive checks,
   warning-light/cluster smoke test, honest verdict scoring, and a strong
   nudge toward a paid pre-purchase inspection and VIN history report.
7. `teen-driver-agreement.pdf` — two-way signed family pact (driver promises
   / grown-up promises), baseline-copied from state GDL laws, review date.

Project layout:

- `src/` — one HTML file per sheet + shared print-safe CSS (`base.css`:
  no web fonts, no external images, print checkboxes rendered as borders).
- `build.py` — one-command local build using WeasyPrint (`--clean`,
  `--only` supported).
- `printables/` — the seven built PDFs.
- `tests/` — pytest suite.
- `README.md`, `LICENSE` (MIT, Copyright (c) 2026 Asdale Dynamics, LLC).

## How to run it

```bash
python3 build.py            # builds all PDFs into printables/
python3 -m pytest tests/ -q # verification suite
```

Only dependencies: Python 3 + `weasyprint` (build), `pypdf` + `pytest`
(tests). Everything renders locally; there are no accounts, no network
calls, and no secrets or personal data in the repo.

## Verification results

- `python3 build.py` → 7/7 PDFs built successfully (see sizes in build log).
- `python3 -m pytest tests/ -q` → **22 passed, 0 failed**, covering:
  - every sheet re-renders to a valid PDF (`%PDF-` header via pypdf),
  - every PDF has ≥ 2 pages (intro page + sheet),
  - the PDF's first page text contains the sheet's title,
  - every sheet includes a "Verify with your manual" reminder and a
    `getting-started` intro page,
  - the real `build.py` invocation succeeds and emits all seven named PDFs.
- Visual spot-check of rendered pages (pdftoppm → PNG review): intro pages,
  fill-in tables, two-column checklists, and footers render cleanly.

## Known gaps / honest notes

- PDF text extraction shows kerning artifacts (e.g. "T een-Driver") — purely
  an extraction quirk; the rendered pages are correct. Tests normalize for it.
- Font embedding makes a few PDFs chunky (300–450 KB); fine for print, could
  be slimmed with a font subsetter if ever needed.
- Packets are US Letter with A4-safe margins; exact A4 sizing untested.
- Content is household common sense plus manual-law reminders — deliberately
  not mechanical advice; each packet points the reader to their own manual,
  state DMV (GDL laws), and paid pre-purchase inspections for the big calls.
- Road-trip and winter pages assume US-style conventions (USPS hold, quarter
  tread test, PSI); internationalization is future work.

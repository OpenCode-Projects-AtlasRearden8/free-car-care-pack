# Free Car Care Pack

Free, unbranded, print-at-home car printables for the family vehicle — from
Asdale Dynamics, LLC. Seven friendly PDF packets, each one opening with a
"getting started" page written the way a friend would explain it, and each one
building in a **verify with your manual** reminder, because every car is a
little different and your owner's manual is the source of truth.

Everything is local-first: plain HTML + CSS sources, one tiny Python build
script, no accounts, no tracking, no network calls, no secrets, no personal
data in the repo.

## What's inside

Each entry below is one PDF packet (intro page + printable pages):

| PDF | What it's for |
| --- | --- |
| `maintenance-schedule.pdf` | Fill-in service calendar you copy **from your own manual**, plus odometer log |
| `service-visit-log.pdf` | One-row-per-visit receipt & history log for every oil change and repair |
| `glovebox-info-card.pdf` | Two-sided emergency card: numbers, breakdown steps, fender-bender steps |
| `winter-car-kit.pdf` | Build-the-kit trunk checklist (★ = budget basics) + one-evening winterize list |
| `road-trip-day-of-checks.pdf` | The week-before prep and the 15-minute departure-morning walk-around |
| `used-car-checklist.pdf` | Pre-purchase look-over and test-drive checks, red-flag spotting, scoring |
| `teen-driver-agreement.pdf` | A signed two-ways family pact (driver promises / grown-up promises), GDL-aware |

## How to build

Requirements: Python 3 with `weasyprint` installed (all rendering is local),
optionally `pypdf` for the tests.

```bash
python3 build.py                 # build all PDFs into printables/
python3 build.py --clean         # remove printables/*.pdf
python3 build.py --only glovebox # build just matching sheets
```

Print the PDFs at 100% scale on US Letter (A4 works fine too). Each packet's
page 1 is the quick-start guide; the printable sheet starts on page 2.

To edit a sheet, just change the HTML in `src/` — pages are plain HTML with a
shared `src/base.css` (print-safe: no web fonts, no external images) — and run
`python3 build.py` again.

## Tests

```bash
python3 -m pytest tests/ -q
```

The tests re-render every sheet and verify (with `pypdf`) that each produces a
valid multi-page PDF containing its title, that every sheet includes a
"Verify with your manual" reminder and a getting-started page, and that
`python3 build.py` itself succeeds and emits all seven PDFs.

## Folder layout

```
build.py                     one-command local build (WeasyPrint)
src/                         one HTML file per sheet + shared print CSS
printables/                  the built, unbranded PDFs (generated)
tests/                       pytest suite verifying every sheet builds a valid PDF
```

## License

MIT — free to print, share, and use. See [`LICENSE`](LICENSE).
Copyright (c) 2026 Asdale Dynamics, LLC.

This project is part of Asdale Dynamics, LLC's beginner-friendly tooling —
plain-English, step-by-step, never condescending, tested before it ships.

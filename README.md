# Subcalc

A small CLI tool to calculate subcontractor retention and discount, generate a printable front sheet, and append CSV lines for Xero import.

Features
- Default rates: 5% retention, 2.5% discount (overridable per invoice)
- Two methods: on-gross or sequential (gross then discount)
- Generates an HTML front sheet to print or save as PDF
- Appends lines to a running CSV for import into Xero (headers customizable later)

Quick Start
1. Ensure Python 3.9+ is installed.
2. Run: `python -m subcalc --help`
3. Example:
   - `python -m subcalc --supplier "ACME Ltd" --invoice 12345 --date 2025-09-05 --gross 10000 --desc "Labour August" --method gross --csv-lines split`

Outputs
- Front sheet: `output/frontsheets/frontsheet_<invoice>.html`
- CSV ledger: `output/xero_import.csv`

Notes
- The CSV header is a reasonable default; if your Xero import needs a different shape, we can adapt via a simple JSON mapping in a future step.

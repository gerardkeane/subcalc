from __future__ import annotations

import argparse
import os
from decimal import Decimal, InvalidOperation

from .models import InvoiceInput
from .calculator import calculate
from .frontsheet import save_frontsheet
from .csv_export import build_csv_rows, append_to_csv


def parse_decimal(val: str, as_percent: bool = False) -> Decimal:
    try:
        d = Decimal(val)
    except InvalidOperation:
        raise argparse.ArgumentTypeError(f"Invalid decimal value: {val}")
    if as_percent:
        # Accept inputs like 5 or 5% or 0.05
        s = str(val).strip().rstrip('%')
        try:
            x = Decimal(s)
        except InvalidOperation:
            raise argparse.ArgumentTypeError(f"Invalid percent: {val}")
        if x > 1:
            return (x / Decimal(100))
        return x
    return d


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="subcalc",
        description="Calculate subcontractor retention and discount; generate front sheet and CSV.",
    )
    p.add_argument("--supplier", required=True, help="Supplier name")
    p.add_argument("--invoice", required=True, help="Invoice number")
    p.add_argument("--date", required=True, help="Invoice date (YYYY-MM-DD)")
    p.add_argument("--gross", required=True, type=parse_decimal, help="Gross amount")
    p.add_argument("--desc", required=True, help="Line description")
    p.add_argument("--retention-rate", default="0.05", type=lambda s: parse_decimal(s, as_percent=True), help="Retention rate (e.g., 5 or 0.05)")
    p.add_argument("--discount-rate", default="0.025", type=lambda s: parse_decimal(s, as_percent=True), help="Discount rate (e.g., 2.5 or 0.025)")
    p.add_argument("--method", choices=["gross", "sequential"], default="gross", help="Calculation method")
    p.add_argument("--csv-lines", choices=["single", "split", "net-only"], default="split", help="CSV output mode")
    p.add_argument("--invoice-pdf", help="Path to original invoice PDF (optional, for reference only)")
    p.add_argument("--out-dir", default="output", help="Base output directory")
    p.add_argument("--frontsheet-dir", default=None, help="Override frontsheet subfolder (default: output/frontsheets)")
    p.add_argument("--csv-path", default=None, help="Override CSV path (default: output/xero_import.csv)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    inv = InvoiceInput(
        supplier=args.supplier,
        invoice_number=args.invoice,
        invoice_date=args.date,
        gross=Decimal(args.gross),
        description=args.desc,
        retention_rate=Decimal(args.retention_rate),
        discount_rate=Decimal(args.discount_rate),
        method=args.method,
        csv_lines=args.csv_lines,
        invoice_pdf=args.invoice_pdf,
    )

    res = calculate(inv)

    # Front sheet
    fs_dir = args.frontsheet_dir or os.path.join(args.out_dir, "frontsheets")
    fs_path = save_frontsheet(inv, res, fs_dir)

    # CSV export
    csv_path = args.csv_path or os.path.join(args.out_dir, "xero_import.csv")
    rows = build_csv_rows(inv, res)
    append_to_csv(rows, csv_path)

    print("Front sheet:", fs_path)
    print("CSV updated:", csv_path)
    print("Net payable:", f"£{res.net:,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


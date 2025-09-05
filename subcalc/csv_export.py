from __future__ import annotations

import csv
import os
from decimal import Decimal
from typing import List, Dict

from .models import InvoiceInput, CalculationResult


# Default CSV header chosen for flexibility; can be adapted later.
CSV_HEADERS = [
    "Supplier",
    "InvoiceNumber",
    "InvoiceDate",
    "LineType",  # Gross, Retention, Discount, Net
    "Description",
    "Amount",
    "AccountCode",
    "TaxType",
]


def _fmt(x: Decimal) -> str:
    return f"{x:.2f}"


def build_csv_rows(inv: InvoiceInput, res: CalculationResult) -> List[Dict[str, str]]:
    base = {
        "Supplier": inv.supplier,
        "InvoiceNumber": inv.invoice_number,
        "InvoiceDate": inv.invoice_date,
        "Description": inv.description,
        "AccountCode": (inv.lines[0].account_code if (inv.lines and inv.lines[0].account_code) else ""),
        "TaxType": (inv.lines[0].tax_type if (inv.lines and inv.lines[0].tax_type) else ""),
    }

    rows: List[Dict[str, str]] = []

    if inv.csv_lines == "single":
        rows.append({
            **base,
            "LineType": "Net",
            "Amount": _fmt(res.net),
        })
        return rows

    if inv.csv_lines == "net-only":
        # Alias of single; sometimes Xero imports expect only a single line.
        rows.append({
            **base,
            "LineType": "Net",
            "Amount": _fmt(res.net),
        })
        return rows

    # split: produce Gross, Retention (negative), Discount (negative)
    rows.append({**base, "LineType": "Gross", "Amount": _fmt(inv.gross)})
    rows.append({**base, "LineType": "Retention", "Amount": _fmt(Decimal(0) - res.retention)})
    rows.append({**base, "LineType": "Discount", "Amount": _fmt(Decimal(0) - res.discount)})
    return rows


def append_to_csv(rows: List[Dict[str, str]], out_csv_path: str) -> None:
    os.makedirs(os.path.dirname(out_csv_path), exist_ok=True)
    file_exists = os.path.exists(out_csv_path)
    with open(out_csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        for r in rows:
            writer.writerow(r)


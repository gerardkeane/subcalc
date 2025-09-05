from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Literal, Optional


CalcMethod = Literal["gross", "sequential"]
CsvLinesMode = Literal["single", "split", "net-only"]


@dataclass
class LineItem:
    description: str
    amount: Decimal  # gross allocation (optional usage in future)
    account_code: Optional[str] = None
    tax_type: Optional[str] = None


@dataclass
class InvoiceInput:
    supplier: str
    invoice_number: str
    invoice_date: str  # ISO date string YYYY-MM-DD
    gross: Decimal
    description: str
    retention_rate: Decimal  # e.g., Decimal("0.05")
    discount_rate: Decimal  # e.g., Decimal("0.025")
    method: CalcMethod
    csv_lines: CsvLinesMode
    invoice_pdf: Optional[str] = None
    lines: Optional[List[LineItem]] = None


@dataclass
class CalculationResult:
    retention: Decimal
    discount: Decimal
    subtotal_after_retention: Decimal
    net: Decimal


from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP, getcontext
from .models import InvoiceInput, CalculationResult


# Set a sensible precision for currency math
getcontext().prec = 28


def _q(amount: Decimal) -> Decimal:
    """Quantize to 2 decimal places with standard rounding."""
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate(inv: InvoiceInput) -> CalculationResult:
    gross = inv.gross
    r = inv.retention_rate
    d = inv.discount_rate

    if inv.method == "gross":
        retention = _q(gross * r)
        discount = _q(gross * d)
        subtotal_after_retention = _q(gross - retention)
        net = _q(gross - retention - discount)
    elif inv.method == "sequential":
        retention = _q(gross * r)
        subtotal_after_retention = _q(gross - retention)
        discount = _q(subtotal_after_retention * d)
        net = _q(subtotal_after_retention - discount)
    else:
        raise ValueError(f"Unknown method: {inv.method}")

    return CalculationResult(
        retention=retention,
        discount=discount,
        subtotal_after_retention=subtotal_after_retention,
        net=net,
    )


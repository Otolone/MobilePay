"""Money helpers.

Wallet balances and transaction amounts are stored as SQL NUMERIC and surface
as ``decimal.Decimal`` in Python. Two rules keep the codebase consistent:

  * For arithmetic, coerce any incoming amount with ``to_decimal`` first.
    ``Decimal + float`` raises TypeError, so a float amount from a request body
    must be converted before it touches a balance.
  * For JSON responses, wrap balances with ``to_amount`` (a float). Flask
    serializes a raw ``Decimal`` as a JSON *string* ("10.50"), which would
    silently change the API contract from number to string.
"""

from decimal import Decimal, ROUND_HALF_UP

_CENTS = Decimal("0.01")


def to_decimal(value) -> Decimal:
    """Coerce a numeric/str amount to a 2-decimal-place Decimal for money math."""
    return Decimal(str(value)).quantize(_CENTS, rounding=ROUND_HALF_UP)


def to_amount(value) -> float:
    """Coerce a Decimal/numeric balance to a float for JSON responses."""
    return float(value)

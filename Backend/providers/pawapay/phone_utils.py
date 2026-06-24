import re, math
from providers.pawapay.config import PawaPayConfig

_PREFIX_RULES = [
    ("23765",  "MTN"),
    ("237670", "MTN"), ("237671", "MTN"), ("237672", "MTN"), ("237673", "MTN"),
    ("237674", "MTN"), ("237675", "MTN"), ("237676", "MTN"), ("237677", "MTN"),
    ("237678", "MTN"), ("237679", "MTN"),
    ("237680", "MTN"), ("237681", "MTN"), ("237682", "MTN"), ("237683", "MTN"),
    ("237684", "MTN"), ("237685", "MTN"), ("237686", "MTN"), ("237687", "MTN"),
    ("237688", "MTN"), ("237689", "MTN"),
    ("237655", "ORANGE"), ("237656", "ORANGE"), ("237657", "ORANGE"),
    ("237658", "ORANGE"), ("237659", "ORANGE"),
    ("237690", "ORANGE"), ("237691", "ORANGE"), ("237692", "ORANGE"),
    ("237693", "ORANGE"), ("237694", "ORANGE"), ("237695", "ORANGE"),
    ("237696", "ORANGE"), ("237697", "ORANGE"), ("237698", "ORANGE"),
    ("237699", "ORANGE"),
]

# Sort once at module load — longest prefix wins (Orange 237655 beats MTN 23765)
_SORTED_PREFIX_RULES = sorted(_PREFIX_RULES, key=lambda r: len(r[0]), reverse=True)

# Upper bound: PawaPay/XAF practical max per transaction (10 million XAF)
XAF_MAX_AMOUNT = 10_000_000


def normalize_msisdn(raw_phone: str) -> str | None:
    """
    Normalize a phone number to the 237XXXXXXXXX format PawaPay expects.
    Accepts: +237xxxxxxxxx / 237xxxxxxxxx / xxxxxxxxx (9 digits)
    Returns None if invalid.
    """
    digits = re.sub(r"\D", "", raw_phone)

    if digits.startswith("237"):
        msisdn = digits
    elif len(digits) == 9:
        msisdn = "237" + digits
    else:
        return None

    if len(msisdn) != 12:
        return None

    return msisdn


def detect_correspondent(raw_phone: str) -> str | None:
    """
    Return 'MTN_MOMO_CMR' or 'ORANGE_CMR' for a Cameroon number, or None.
    Uses pre-sorted prefix list — no re-sort on every call.
    """
    msisdn = normalize_msisdn(raw_phone)
    if not msisdn:
        return None

    for prefix, network in _SORTED_PREFIX_RULES:
        if msisdn.startswith(prefix):
            return PawaPayConfig.CORRESPONDENTS.get(network)

    return None


def validate_amount_for_cameroon(amount) -> tuple[bool, str]:
    """
    XAF must be a positive whole number within the allowed range.
    Returns (is_valid, error_message).
    """
    try:
        numeric = float(amount)
    except (TypeError, ValueError):
        return False, "Amount must be a number"

    if math.isinf(numeric) or math.isnan(numeric):
        return False, "Amount must be a finite number"

    if numeric <= 0:
        return False, "Amount must be greater than zero"

    if numeric != int(numeric):
        return False, (
            f"XAF does not support decimal amounts. "
            f"Use a whole number (e.g. {int(numeric)})."
        )

    if int(numeric) > XAF_MAX_AMOUNT:
        return False, (
            f"Amount exceeds maximum allowed per transaction "
            f"({XAF_MAX_AMOUNT:,} XAF)."
        )

    return True, ""

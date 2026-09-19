import random
import string
from datetime import datetime, timezone


def generate_complaint_id(prefix: str = "CR") -> str:
    """Generate a unique human-readable complaint identifier, e.g., CR-202609-AB12."""
    date_part = datetime.now(timezone.utc).strftime("%Y%m")
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{prefix}-{date_part}-{random_part}"


def generate_transaction_id(prefix: str = "TXN") -> str:
    """Generate a unique transaction identifier, e.g., TXN-2026-XYZ987."""
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{date_part}-{random_part}"


def mask_sensitive_text(text: str, visible_chars: int = 4) -> str:
    """Mask account/card numbers or phone numbers to prevent unnecessary PII storage."""
    if not text:
        return ""
    if len(text) <= visible_chars:
        return "*" * len(text)
    return "*" * (len(text) - visible_chars) + text[-visible_chars:]


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Check if latitude and longitude are within standard geographical boundaries."""
    return -90.0 <= latitude <= 90.0 and -180.0 <= longitude <= 180.0

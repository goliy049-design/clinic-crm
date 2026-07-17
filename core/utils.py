import uuid


def generate_reference_code(prefix: str = "REF") -> str:
    """Generate a short, human-friendly reference code, e.g. for invoices
    or appointment confirmations: 'APT-3F9A21BC'."""
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

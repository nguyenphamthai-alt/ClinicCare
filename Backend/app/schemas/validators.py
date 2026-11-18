import uuid


def validate_uuid4(value: str, field_name: str) -> str:
    try:
        parsed = uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"{field_name} must be a valid UUID")
    if parsed.version != 4:
        raise ValueError(f"{field_name} must be a UUID v4")
    return str(parsed)

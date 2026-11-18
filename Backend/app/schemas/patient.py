import uuid
from typing import Optional

from pydantic import BaseModel, field_validator


def _validate_uuid4(value: str, field_name: str) -> str:
    try:
        parsed = uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"{field_name} must be a valid UUID")
    if parsed.version != 4:
        raise ValueError(f"{field_name} must be a UUID v4")
    return str(parsed)


class PatientOut(BaseModel):
    id: str
    full_name: str
    date_of_birth: Optional[str] = None
    sex: str
    phone: Optional[str] = None
    email: Optional[str] = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        return _validate_uuid4(value, "id")

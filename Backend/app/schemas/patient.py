import uuid
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


def _validate_uuid4(value: str, field_name: str) -> str:
    try:
        parsed = uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"{field_name} must be a valid UUID")
    if parsed.version != 4:
        raise ValueError(f"{field_name} must be a UUID v4")
    return str(parsed)


class PatientCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    sex: Literal["Male", "Female"]
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9 \-]{7,15}$")
    email: Optional[EmailStr] = None

    @field_validator("full_name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("full_name must not be blank")
        return v


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

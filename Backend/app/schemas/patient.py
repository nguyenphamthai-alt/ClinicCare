from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.schemas.validators import validate_uuid4


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
        return validate_uuid4(value, "id")


class PatientCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    date_of_birth: Optional[str] = None
    sex: Literal["Male", "Female"]
    phone: Optional[str] = Field(default=None, max_length=30)
    email: Optional[str] = Field(default=None, max_length=200)

    @field_validator("full_name")
    @classmethod
    def strip_full_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("full_name must not be blank")
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            parsed = date.fromisoformat(value.strip())
        except (AttributeError, ValueError):
            raise ValueError("date_of_birth must be a valid date in YYYY-MM-DD format")
        if parsed > date.today():
            raise ValueError("date_of_birth must not be in the future")
        return parsed.isoformat()

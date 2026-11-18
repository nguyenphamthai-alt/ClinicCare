from typing import Optional

from pydantic import BaseModel, field_validator

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

import uuid
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


def _validate_uuid4(value: str, field_name: str) -> str:
    try:
        parsed = uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"{field_name} must be a valid UUID")
    if parsed.version != 4:
        raise ValueError(f"{field_name} must be a UUID v4")
    return str(parsed)


class ConsultationCreate(BaseModel):
    patient_id: str
    treatment_notes: str = Field(min_length=1, max_length=5000)
    diagnosis_codes: list[str] = Field(min_length=1, max_length=20)
    primary_code: Optional[str] = None
    status: Literal["draft", "completed", "cancelled"] = "completed"

    @field_validator("patient_id")
    @classmethod
    def validate_patient_id(cls, value: str) -> str:
        return _validate_uuid4(value, "patient_id")

    @field_validator("treatment_notes")
    @classmethod
    def strip_notes(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("treatment_notes must not be blank")
        return v

    @model_validator(mode="after")
    def check_codes(self):
        codes = list(dict.fromkeys(c.strip().upper() for c in self.diagnosis_codes))
        self.diagnosis_codes = codes
        if self.primary_code is None:
            self.primary_code = codes[0]
        else:
            self.primary_code = self.primary_code.strip().upper()
            if self.primary_code not in codes:
                raise ValueError("primary_code must be one of diagnosis_codes")
        return self


class ConsultationDiagnosis(BaseModel):
    code: str
    description: str
    is_primary: bool


class ConsultationOut(BaseModel):
    id: str
    consultation_date: str
    treatment_notes: str
    status: str
    patient_id: str
    patient_name: str
    doctor_name: str
    diagnoses: list[ConsultationDiagnosis]

    @field_validator("id", "patient_id")
    @classmethod
    def validate_uuid_fields(cls, value: str, info) -> str:
        return _validate_uuid4(value, info.field_name)

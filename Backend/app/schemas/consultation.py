from datetime import date, datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.validators import validate_uuid4


class ConsultationCreate(BaseModel):
    patient_id: str
    treatment_notes: str = Field(min_length=1, max_length=5000)
    diagnosis_codes: list[str] = Field(min_length=1, max_length=10)
    primary_code: Optional[str] = None
    consultation_date: Optional[date] = None

    @field_validator("consultation_date")
    @classmethod
    def validate_consultation_date(cls, value: Optional[date]) -> Optional[date]:
        if value is None:
            return None
        if value > date.today() + timedelta(days=1):
            raise ValueError("consultation_date must not be later than tomorrow")
        return value

    @field_validator("patient_id")
    @classmethod
    def validate_patient_id(cls, value: str) -> str:
        return validate_uuid4(value, "patient_id")

    @field_validator("treatment_notes")
    @classmethod
    def strip_notes(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("treatment_notes must not be blank")
        return v

    @model_validator(mode="after")
    def check_codes(self):
        codes = [c.strip().upper() for c in self.diagnosis_codes]
        if len(codes) != len(set(codes)):
            raise ValueError("diagnosis_codes must not contain duplicates")
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
    patient_id: str
    patient_name: str
    doctor_name: str
    diagnoses: list[ConsultationDiagnosis]

    @field_validator("id", "patient_id")
    @classmethod
    def validate_uuid_fields(cls, value: str, info) -> str:
        return validate_uuid4(value, info.field_name)

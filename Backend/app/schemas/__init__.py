from app.schemas.auth import LoginIn, RefreshIn, TokenOut
from app.schemas.consultation import ConsultationCreate, ConsultationDiagnosis, ConsultationOut
from app.schemas.diagnosis import DiagnosisOut
from app.schemas.patient import PatientOut

__all__ = [
    "LoginIn",
    "RefreshIn",
    "TokenOut",
    "PatientOut",
    "DiagnosisOut",
    "ConsultationCreate",
    "ConsultationDiagnosis",
    "ConsultationOut",
]

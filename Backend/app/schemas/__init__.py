from app.schemas.auth import AuthOut, LoginIn
from app.schemas.consultation import ConsultationCreate, ConsultationDiagnosis, ConsultationOut
from app.schemas.diagnosis import DiagnosisOut
from app.schemas.patient import PatientOut

__all__ = [
    "LoginIn",
    "AuthOut",
    "PatientOut",
    "DiagnosisOut",
    "ConsultationCreate",
    "ConsultationDiagnosis",
    "ConsultationOut",
]

import re
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.db import get_db
from app.core.security import current_doctor
from app.schemas.consultation import ConsultationCreate, ConsultationOut
from app.services.consultation_service import ConsultationService

router = APIRouter(tags=["consultations"])
service = ConsultationService()


@router.post("/consultation", response_model=ConsultationOut, status_code=201)
def create_consultation(
    body: ConsultationCreate, db=Depends(get_db), doctor=Depends(current_doctor)
):
    return service.create(db, body.patient_id, doctor["id"], body)


@router.get("/consultation", response_model=list[ConsultationOut])
def list_consultations(
    patient_id: Optional[str] = Query(None, max_length=36),
    patient_name: Optional[str] = Query(None, max_length=100),
    doctor_id: Optional[str] = Query(None, max_length=36),
    doctor_name: Optional[str] = Query(None, max_length=100),
    diagnosis_code: Optional[str] = Query(None, max_length=50),
    search: Optional[str] = Query(None, max_length=200),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db=Depends(get_db),
    _=Depends(current_doctor),
):
    filters = {}

    if patient_id is not None:
        try:
            filters["patient_id"] = str(uuid.UUID(patient_id))
        except ValueError:
            raise HTTPException(status_code=422, detail="patient_id must be a valid UUID v4")
    if patient_name is not None and patient_name.strip():
        filters["patient_name"] = patient_name.strip()
    if doctor_id is not None:
        try:
            filters["doctor_id"] = str(uuid.UUID(doctor_id))
        except ValueError:
            raise HTTPException(status_code=422, detail="doctor_id must be a valid UUID v4")
    if doctor_name is not None and doctor_name.strip():
        filters["doctor_name"] = doctor_name.strip()
    if diagnosis_code is not None and diagnosis_code.strip():
        filters["diagnosis_code"] = diagnosis_code.strip()
    if search is not None and search.strip():
        filters["search"] = search.strip()

    return service.list(db, filters, limit, offset)

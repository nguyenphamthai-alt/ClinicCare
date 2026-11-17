from fastapi import APIRouter, Depends, Query

from app.core.db import get_db
from app.core.security import current_doctor
from app.schemas.patient import PatientOut
from app.services.patient_service import PatientService

router = APIRouter(tags=["patients"])
service = PatientService()


@router.get("/patients", response_model=list[PatientOut])
def search_patients(
    search: str = Query("", max_length=100),
    limit: int = Query(20, ge=1, le=100),
    db=Depends(get_db),
    _=Depends(current_doctor),
):
    return service.search(db, search, limit)


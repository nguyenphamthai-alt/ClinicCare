from fastapi import APIRouter, Depends, Query

from app.core.db import get_db
from app.core.security import current_doctor
from app.schemas.diagnosis import DiagnosisOut
from app.services.diagnosis_service import DiagnosisService

router = APIRouter(tags=["diagnosis"])
service = DiagnosisService()


@router.get("/diagnosis", response_model=list[DiagnosisOut])
def search_diagnosis(
    search: str = Query("", max_length=100),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db=Depends(get_db),
    _=Depends(current_doctor),
):
    return service.search(db, search, limit, offset)

import sqlite3

from fastapi import HTTPException

from app.repositories.consultation_repository import ConsultationRepository


class ConsultationService:
    def __init__(self, consultation_repository: ConsultationRepository | None = None):
        self.consultation_repository = consultation_repository or ConsultationRepository()

    def create(self, db, patient_id: str, doctor_id: str, body):
        if not self.consultation_repository.validate_patient(db, patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")

        codes = body.diagnosis_codes
        found = self.consultation_repository.find_diagnosis_codes(db, codes)
        missing = [c for c in codes if c not in found]
        if missing:
            raise HTTPException(status_code=422, detail=f"Unknown diagnosis codes: {', '.join(missing)}")

        try:
            cid = self.consultation_repository.create(
                db,
                patient_id,
                doctor_id,
                body.treatment_notes,
                body.status,
                codes,
                body.primary_code,
                body.consultation_date,
            )
        except sqlite3.Error:
            db.rollback()
            raise HTTPException(status_code=500, detail="Could not save consultation")

        return self.consultation_repository.find_by_id(db, cid)

    def list(self, db, filters, limit: int, offset: int):
        return self.consultation_repository.list_with_diagnoses(db, filters, limit, offset)

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
            )
        except sqlite3.Error:
            db.rollback()
            raise HTTPException(status_code=500, detail="Could not save consultation")

        return self.consultation_repository.find_by_id(db, cid)

    def list(self, db, filters, limit: int, offset: int):
        # Build each SQL filter together with its bound parameter so filters remain safe and aligned with the query.
        where, params = [], []
        if filters.get("patient_id") is not None:
            where.append("c.patient_id = ?")
            params.append(filters["patient_id"])
        if filters.get("patient_name"):
            where.append("LOWER(p.full_name) LIKE LOWER(?)")
            params.append(f"%{filters['patient_name']}%")
        if filters.get("doctor_id") is not None:
            where.append("c.doctor_id = ?")
            params.append(filters["doctor_id"])
        if filters.get("doctor_name"):
            where.append("LOWER(d.full_name) LIKE LOWER(?)")
            params.append(f"%{filters['doctor_name']}%")
        if filters.get("diagnosis_code"):
            normalized_code = filters["diagnosis_code"].strip().upper()
            if "." in normalized_code:
                where.append(
                    "EXISTS (SELECT 1 FROM consultation_diagnoses cd "
                    "WHERE cd.consultation_id = c.id AND cd.diagnosis_code = ?)"
                )
                params.append(normalized_code)
            else:
                where.append(
                    "EXISTS (SELECT 1 FROM consultation_diagnoses cd "
                    "WHERE cd.consultation_id = c.id AND cd.diagnosis_code LIKE ?)"
                )
                params.append(f"{normalized_code}%")
        if filters.get("search"):
            term = filters["search"].strip()
            where.append(
                "(LOWER(p.full_name) LIKE LOWER(?) OR LOWER(c.treatment_notes) LIKE LOWER(?) "
                "OR EXISTS (SELECT 1 FROM consultation_diagnoses cd "
                "JOIN diagnosis_codes dc ON dc.code = cd.diagnosis_code "
                "WHERE cd.consultation_id = c.id AND (LOWER(dc.code) LIKE LOWER(?) OR LOWER(dc.description) LIKE LOWER(?))))"
            )
            pattern = f"%{term}%"
            params.extend([pattern, pattern, pattern, pattern])

        sql = self.consultation_repository.BASE_SQL
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY c.consultation_date DESC, c.id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        return self.consultation_repository.list_with_diagnoses(db, sql, params)

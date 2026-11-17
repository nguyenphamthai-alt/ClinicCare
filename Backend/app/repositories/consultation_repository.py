import sqlite3

from app.core.db import new_uuid


class ConsultationRepository:
    BASE_SQL = """
        SELECT c.id, c.consultation_date, c.treatment_notes, c.status,
               p.id AS patient_id, p.full_name AS patient_name,
               d.full_name AS doctor_name
        FROM consultations c
        JOIN patients p ON p.id = c.patient_id
        JOIN doctors d ON d.id = c.doctor_id
    """

    @staticmethod
    def _fetch_diagnoses_by_consultation(db, consultation_ids):
        by_id = {consultation_id: [] for consultation_id in consultation_ids}
        if not consultation_ids:
            return by_id

        # Batch-load all diagnoses for the current page so one consultation page does not trigger a per-row N+1 query.
        marks = ",".join("?" * len(consultation_ids))
        for r in db.execute(
            f"""
            SELECT cd.consultation_id, cd.diagnosis_code AS code,
                   dc.description, cd.is_primary
            FROM consultation_diagnoses cd
            JOIN diagnosis_codes dc ON dc.code = cd.diagnosis_code
            WHERE cd.consultation_id IN ({marks})
            ORDER BY cd.is_primary DESC, cd.diagnosis_code
            """,
            consultation_ids,
        ):
            by_id[r["consultation_id"]].append(
                {"code": r["code"], "description": r["description"], "is_primary": bool(r["is_primary"])}
            )
        return by_id

    @staticmethod
    def with_diagnoses(db, rows):
        ids = [r["id"] for r in rows]
        diagnoses_by_id = ConsultationRepository._fetch_diagnoses_by_consultation(db, ids)
        return [{**dict(r), "diagnoses": diagnoses_by_id.get(r["id"], [])} for r in rows]

    def list_with_diagnoses(self, db, sql, params):
        rows = self.list(db, sql, params)
        if not rows:
            return []

        consultation_ids = [r["id"] for r in rows]
        diagnoses_by_id = self._fetch_diagnoses_by_consultation(db, consultation_ids)
        return [{**dict(r), "diagnoses": diagnoses_by_id.get(r["id"], [])} for r in rows]

    def create(self, db, patient_id, doctor_id, treatment_notes, status, diagnosis_codes, primary_code):
        cid = new_uuid()
        db.execute(
            "INSERT INTO consultations (id, patient_id, doctor_id, treatment_notes, status) VALUES (?,?,?,?,?)",
            (cid, patient_id, doctor_id, treatment_notes, status),
        )
        db.executemany(
            "INSERT INTO consultation_diagnoses (id, consultation_id, diagnosis_code, is_primary) VALUES (?,?,?,?)",
            [(new_uuid(), cid, c, int(c == primary_code)) for c in diagnosis_codes],
        )
        db.commit()
        return cid

    def list(self, db, sql, params):
        return db.execute(sql, params).fetchall()

    def validate_patient(self, db, patient_id):
        return db.execute("SELECT 1 FROM patients WHERE id = ?", (patient_id,)).fetchone()

    def find_diagnosis_codes(self, db, codes):
        marks = ",".join("?" * len(codes))
        return {r["code"] for r in db.execute(f"SELECT code FROM diagnosis_codes WHERE code IN ({marks})", codes)}

    def find_by_id(self, db, consultation_id):
        rows = db.execute(self.BASE_SQL + " WHERE c.id = ?", (consultation_id,)).fetchall()
        return self.with_diagnoses(db, rows)[0]

import sqlite3

from app.core.db import new_uuid


class ConsultationRepository:
    # Build the shared consultation response by joining patient and doctor names to the consultation record.
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

        # Load diagnoses for all consultation IDs in one query to avoid one database query per result row.
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

    def list_with_diagnoses(self, db, filters, limit, offset):
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

        sql = self.BASE_SQL
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY c.consultation_date DESC, c.id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = db.execute(sql, params).fetchall()
        if not rows:
            return []

        consultation_ids = [r["id"] for r in rows]
        diagnoses_by_id = self._fetch_diagnoses_by_consultation(db, consultation_ids)
        return [{**dict(r), "diagnoses": diagnoses_by_id.get(r["id"], [])} for r in rows]

    def create(self, db, patient_id, doctor_id, treatment_notes, status, diagnosis_codes, primary_code, consultation_date=None):
        cid = new_uuid()
        if consultation_date:
            db.execute(
                "INSERT INTO consultations (id, patient_id, doctor_id, consultation_date, treatment_notes, status) VALUES (?,?,?,?,?,?)",
                (cid, patient_id, doctor_id, consultation_date, treatment_notes, status),
            )
        else:
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

    def validate_patient(self, db, patient_id):
        return db.execute("SELECT 1 FROM patients WHERE id = ?", (patient_id,)).fetchone()

    def find_diagnosis_codes(self, db, codes):
        marks = ",".join("?" * len(codes))
        return {r["code"] for r in db.execute(f"SELECT code FROM diagnosis_codes WHERE code IN ({marks})", codes)}

    def find_by_id(self, db, consultation_id):
        rows = db.execute(self.BASE_SQL + " WHERE c.id = ?", (consultation_id,)).fetchall()
        return self.with_diagnoses(db, rows)[0]

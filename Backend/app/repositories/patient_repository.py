from app.core.db import new_uuid


class PatientRepository:
    def search(self, db, search_term, limit):
        return db.execute(
            "SELECT * FROM patients WHERE full_name LIKE ? ORDER BY full_name LIMIT ?",
            (f"%{search_term.strip()}%", limit),
        ).fetchall()

    def create(self, db, full_name, date_of_birth, sex, phone, email):
        patient_id = new_uuid()
        db.execute(
            "INSERT INTO patients (id, full_name, date_of_birth, sex, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
            (patient_id, full_name, date_of_birth, sex, phone, email),
        )
        db.commit()
        return patient_id

    def find_by_id(self, db, patient_id):
        row = db.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
        return dict(row) if row else None

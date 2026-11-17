class PatientRepository:
    def search(self, db, search_term, limit):
        return db.execute(
            "SELECT * FROM patients WHERE full_name LIKE ? ORDER BY full_name LIMIT ?",
            (f"%{search_term.strip()}%", limit),
        ).fetchall()

    def create(self, db, patient_data):
        patient_id = patient_data["id"]
        db.execute(
            "INSERT INTO patients (id, full_name, date_of_birth, sex, phone, email) VALUES (?,?,?,?,?,?)",
            (
                patient_id,
                patient_data["full_name"],
                patient_data["date_of_birth"],
                patient_data["sex"],
                patient_data["phone"],
                patient_data["email"],
            ),
        )
        db.commit()
        return db.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()

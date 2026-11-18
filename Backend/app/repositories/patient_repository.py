class PatientRepository:
    def search(self, db, search_term, limit):
        return db.execute(
            "SELECT * FROM patients WHERE full_name LIKE ? ORDER BY full_name LIMIT ?",
            (f"%{search_term.strip()}%", limit),
        ).fetchall()

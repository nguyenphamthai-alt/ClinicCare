class DiagnosisRepository:
    def search(self, db, search_term, limit, offset):
        term = search_term.strip()
        # Match code prefixes at the start and descriptions anywhere in the text, then apply pagination.
        return db.execute(
            """
            SELECT code, description FROM diagnosis_codes
            WHERE code LIKE ? OR description LIKE ?
            ORDER BY code LIMIT ? OFFSET ?
            """,
            (f"{term}%", f"%{term}%", limit, offset),
        ).fetchall()

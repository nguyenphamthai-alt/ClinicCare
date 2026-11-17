from app.core.security import hash_token


class DoctorRepository:
    def get_by_username(self, db, username):
        return db.execute(
            "SELECT id, username, password_hash, full_name FROM doctors WHERE username = ?",
            (username,),
        ).fetchone()

    def get_by_refresh_token(self, db, refresh_token):
        return db.execute(
            "SELECT id, username, full_name, refresh_token_expires_at FROM doctors WHERE refresh_token_hash = ?",
            (hash_token(refresh_token),),
        ).fetchone()

    def update_refresh_token(self, db, doctor_id, refresh_hash, expires):
        db.execute(
            "UPDATE doctors SET refresh_token_hash = ?, refresh_token_expires_at = ? WHERE id = ?",
            (refresh_hash, expires, doctor_id),
        )
        db.commit()

    def clear_refresh_token(self, db, doctor_id):
        db.execute(
            "UPDATE doctors SET refresh_token_hash = NULL, refresh_token_expires_at = NULL WHERE id = ?",
            (doctor_id,),
        )
        db.commit()

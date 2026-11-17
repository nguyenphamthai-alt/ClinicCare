from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.security import create_token, new_refresh_token, verify_password
from app.repositories.doctor_repository import DoctorRepository


class AuthService:
    def __init__(self, doctor_repository: DoctorRepository | None = None):
        self.doctor_repository = doctor_repository or DoctorRepository()

    def issue_tokens(self, db, doctor_id: str, username: str, full_name: str | None = None) -> dict:
        # Refresh tokens are rotated on each auth cycle so expired or leaked tokens cannot stay valid.
        refresh, refresh_hash, expires = new_refresh_token()
        self.doctor_repository.update_refresh_token(db, doctor_id, refresh_hash, expires)
        return {
            "access_token": create_token(doctor_id, username, full_name),
            "refresh_token": refresh,
            "token_type": "bearer",
            "full_name": full_name or username,
        }

    def login(self, db, username: str, password: str) -> dict:
        row = self.doctor_repository.get_by_username(db, username)
        if row is None or not verify_password(password, row["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return self.issue_tokens(db, row["id"], row["username"], row["full_name"])

    def refresh(self, db, refresh_token: str) -> dict:
        row = self.doctor_repository.get_by_refresh_token(db, refresh_token)
        if row is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        expires = datetime.fromisoformat(row["refresh_token_expires_at"])
        if expires < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expired")
        return self.issue_tokens(db, row["id"], row["username"], row["full_name"])

    def logout(self, db, doctor_id: str) -> None:
        self.doctor_repository.clear_refresh_token(db, doctor_id)

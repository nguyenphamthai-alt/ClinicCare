import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.responses import Response

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7

bearer = HTTPBearer(auto_error=False)
ACCESS_COOKIE_NAME = "cliniccare_access_token"
REFRESH_COOKIE_NAME = "cliniccare_refresh_token"


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=ACCESS_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=REFRESH_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_token(doctor_id: str, username: str, full_name: str | None = None) -> str:
    # The JWT carries both the internal doctor id and the display name used by the frontend sidebar.
    payload = {
        "sub": str(doctor_id),
        "username": username,
        "full_name": full_name or username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def new_refresh_token() -> tuple[str, str, str]:
    token = secrets.token_urlsafe(48)
    expires = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE_DAYS)
    return token, hash_token(token), expires.isoformat()


def current_doctor(request: Request, creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    token_value = None
    if creds is not None:
        token_value = creds.credentials
    else:
        token_value = request.cookies.get(ACCESS_COOKIE_NAME)

    if token_value is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        data = jwt.decode(token_value, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {
        "id": str(data["sub"]),
        "username": data["username"],
        "full_name": data.get("full_name", data.get("username")),
    }

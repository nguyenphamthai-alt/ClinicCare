from fastapi import APIRouter, Depends, HTTPException, Request, Response

from app.core.db import get_db
from app.core.security import current_doctor, set_auth_cookies
from app.schemas.auth import AuthOut, LoginIn, RefreshIn
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
service = AuthService()


@router.post("/login", response_model=AuthOut)
def login(body: LoginIn, response: Response, db=Depends(get_db)):
    payload = service.login(db, body.username, body.password)
    set_auth_cookies(response, payload["access_token"], payload["refresh_token"])
    return {"full_name": payload["full_name"]}


@router.get("/me")
def me(doctor=Depends(current_doctor)):
    return {"id": doctor["id"], "username": doctor["username"], "full_name": doctor["full_name"]}


@router.post("/refresh", response_model=AuthOut)
def refresh(request: Request, response: Response, body: RefreshIn | None = None, db=Depends(get_db)):
    refresh_token = body.refresh_token if body and body.refresh_token else request.cookies.get("cliniccare_refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not provided")
    payload = service.refresh(db, refresh_token)
    set_auth_cookies(response, payload["access_token"], payload["refresh_token"])
    return {"full_name": payload["full_name"]}


@router.post("/logout", status_code=204)
def logout(response: Response, db=Depends(get_db), doctor=Depends(current_doctor)):
    service.logout(db, doctor["id"])
    response.delete_cookie("cliniccare_access_token", path="/")
    response.delete_cookie("cliniccare_refresh_token", path="/")
    response.status_code = 204
    return response

from datetime import datetime, timedelta, timezone

from app.core.db import connect


def test_login_with_valid_credentials(client):
    response = client.post(
        "/auth/login",
        json={"username": "doctor01", "password": "@Admin123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["full_name"] == "Dr. Nguyen Minh"
    assert "access_token" not in payload
    assert "refresh_token" not in payload
    assert response.cookies.get("cliniccare_access_token")
    assert response.cookies.get("cliniccare_refresh_token")


def test_login_with_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        json={"username": "doctor01", "password": "not-the-right-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_with_unknown_username(client):
    response = client.post(
        "/auth/login",
        json={"username": "doctor_missing", "password": "@Admin123"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_protected_endpoint_requires_authentication(client):
    response = client.get("/consultation")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_protected_endpoint_accepts_valid_authentication(authenticated_client):
    response = authenticated_client.get("/auth/me")

    assert response.status_code == 200
    payload = response.json()
    assert payload["username"] == "doctor01"
    assert payload["full_name"] == "Dr. Nguyen Minh"


def test_refresh_with_valid_refresh_token(authenticated_client):
    original_refresh_token = authenticated_client.cookies.get("cliniccare_refresh_token")

    response = authenticated_client.post("/auth/refresh")

    assert response.status_code == 200
    payload = response.json()
    assert payload["full_name"] == "Dr. Nguyen Minh"
    assert "access_token" not in payload
    assert "refresh_token" not in payload
    assert authenticated_client.cookies.get("cliniccare_refresh_token") != original_refresh_token
    assert authenticated_client.cookies.get("cliniccare_refresh_token")

    authenticated_client.cookies.clear()
    reuse_response = authenticated_client.post(
        "/auth/refresh",
        headers={"Cookie": f"cliniccare_refresh_token={original_refresh_token}"},
    )
    assert reuse_response.status_code == 401
    assert reuse_response.json()["detail"] == "Invalid refresh token"


def test_refresh_with_invalid_refresh_token(client):
    client.cookies.set("cliniccare_refresh_token", "not-a-valid-refresh-token")
    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token"


def test_refresh_with_expired_refresh_token(authenticated_client):
    with connect() as db:
        db.execute(
            "UPDATE doctors SET refresh_token_expires_at = ? WHERE username = ?",
            ((datetime.now(timezone.utc) - timedelta(days=1)).isoformat(), "doctor01"),
        )

    response = authenticated_client.post("/auth/refresh")

    assert response.status_code == 401
    assert response.json()["detail"] == "Refresh token expired"


def test_refresh_rejects_json_body_token_without_cookie(client):
    login_response = client.post(
        "/auth/login",
        json={"username": "doctor01", "password": "@Admin123"},
    )
    refresh_token = login_response.cookies.get("cliniccare_refresh_token")
    assert refresh_token
    client.cookies.clear()

    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 401
    assert response.json()["detail"] == "Refresh token not provided"


def test_logout_invalidates_refresh_session(client):
    client.post(
        "/auth/login",
        json={"username": "doctor01", "password": "@Admin123"},
    )
    refresh_token = client.cookies.get("cliniccare_refresh_token")

    logout_response = client.post("/auth/logout")

    assert logout_response.status_code == 204
    set_cookie_value = logout_response.headers.get("set-cookie", "")
    assert "cliniccare_access_token=\"\"" in set_cookie_value
    assert "cliniccare_refresh_token=\"\"" in set_cookie_value
    assert "Max-Age=0" in set_cookie_value

    client.cookies.set("cliniccare_refresh_token", refresh_token)
    refresh_response = client.post("/auth/refresh")
    assert refresh_response.status_code == 401
    assert refresh_response.json()["detail"] == "Invalid refresh token"


def test_expired_access_cookie_can_restore_session_with_refresh(authenticated_client):
    authenticated_client.cookies.delete("cliniccare_access_token")

    refresh_response = authenticated_client.post("/auth/refresh")
    assert refresh_response.status_code == 200

    me_response = authenticated_client.get("/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "doctor01"


def test_invalid_refresh_session_cannot_restore_profile(client):
    client.cookies.set("cliniccare_refresh_token", "not-a-valid-refresh-token")

    assert client.post("/auth/refresh").status_code == 401
    assert client.get("/auth/me").status_code == 401

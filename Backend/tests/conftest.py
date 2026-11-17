import os
import sqlite3
import tempfile
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.db import init_db
from app.main import app

DB_DIR = Path(__file__).resolve().parents[1] / "database"


@pytest.fixture(scope="session", autouse=True)
def set_test_db_env():
    if "CLINICCARE_DB_PATH" not in os.environ:
        os.environ["CLINICCARE_DB_PATH"] = os.path.join(
            tempfile.gettempdir(), f"cliniccare_test_{uuid.uuid4()}.db"
        )
    yield
    db_path = os.environ.get("CLINICCARE_DB_PATH")
    if db_path:
        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


@pytest.fixture
def seeded_db():
    db_path = Path(os.environ["CLINICCARE_DB_PATH"])
    if db_path.exists():
        with sqlite3.connect(db_path) as conn:
            has_schema = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='doctors'"
            ).fetchone()
        if not has_schema:
            db_path.unlink()
    init_db()

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.execute("DELETE FROM consultation_diagnoses")
        conn.execute("DELETE FROM consultations")
        conn.execute("DELETE FROM diagnosis_codes")
        conn.execute("DELETE FROM patients")
        conn.execute("DELETE FROM doctors")
        conn.executescript((DB_DIR / "seed_diagnosis.sql").read_text(encoding="utf-8"))
        conn.executescript((DB_DIR / "seed.sql").read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()
    yield


@pytest.fixture
def client(seeded_db):
    app.dependency_overrides.clear()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(client):
    response = client.post(
        "/auth/login",
        json={"username": "doctor01", "password": "@Admin123"},
    )
    assert response.status_code == 200, response.text
    yield client

import os
import sqlite3
import uuid
from datetime import date, timedelta
from pathlib import Path

import pytest


PATIENT_ID = "271ae31d-1a31-4dfa-9d3a-8d3e2e46b101"


@pytest.fixture
def consultation_payload():
    return {
        "patient_id": PATIENT_ID,
        "treatment_notes": "Patient reports fever and mild cough after travel.",
        "diagnosis_codes": ["A00.0", "A00.1"],
        "primary_code": "A00.0"
    }


def test_create_consultation_successfully(authenticated_client, consultation_payload):
    response = authenticated_client.post("/consultation", json=consultation_payload)

    assert response.status_code == 201
    payload = response.json()
    assert payload["patient_id"] == PATIENT_ID
    assert "status" not in payload
    assert payload["treatment_notes"] == consultation_payload["treatment_notes"]
    assert payload["consultation_date"] == date.today().isoformat()

    db_path = Path(os.environ["CLINICCARE_DB_PATH"])

    with sqlite3.connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM consultations WHERE id = ?", (payload["id"],)).fetchone()[0]
    assert count == 1


def test_create_consultation_with_unknown_patient_returns_404(authenticated_client):
    payload = {
        "patient_id": str(uuid.uuid4()),
        "treatment_notes": "Patient has a repeated checkup request.",
        "diagnosis_codes": ["A00.0"],
        "primary_code": "A00.0",
    }

    response = authenticated_client.post("/consultation", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_create_consultation_with_invalid_diagnosis_code_returns_422(authenticated_client):
    payload = {
        "patient_id": PATIENT_ID,
        "treatment_notes": "Patient reports fever and mild cough after travel.",
        "diagnosis_codes": ["NOT_A_REAL_CODE"],
        "primary_code": "NOT_A_REAL_CODE",
    }

    response = authenticated_client.post("/consultation", json=payload)

    assert response.status_code == 422
    assert "Unknown diagnosis codes" in response.json()["detail"]


def test_create_consultation_requires_primary_code_to_be_in_diagnosis_list(authenticated_client):
    payload = {
        "patient_id": PATIENT_ID,
        "treatment_notes": "Patient reports fever and mild cough after travel.",
        "diagnosis_codes": ["A00.0", "A00.1"],
        "primary_code": "J00",
    }

    response = authenticated_client.post("/consultation", json=payload)

    assert response.status_code == 422


def test_create_consultation_rejects_blank_treatment_notes(authenticated_client):
    payload = {
        "patient_id": PATIENT_ID,
        "treatment_notes": "   ",
        "diagnosis_codes": ["A00.0"],
        "primary_code": "A00.0",
    }

    response = authenticated_client.post("/consultation", json=payload)

    assert response.status_code == 422


def test_consultation_create_requires_authentication(client):
    payload = {
        "patient_id": PATIENT_ID,
        "treatment_notes": "This should not be created without a login.",
        "diagnosis_codes": ["A00.0"],
        "primary_code": "A00.0",
    }

    response = client.post("/consultation", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_consultation_with_selected_historical_date(authenticated_client, consultation_payload):
    consultation_payload["consultation_date"] = "2024-02-29"

    response = authenticated_client.post("/consultation", json=consultation_payload)

    assert response.status_code == 201
    payload = response.json()
    assert payload["consultation_date"] == "2024-02-29"

    db_path = Path(os.environ["CLINICCARE_DB_PATH"])
    with sqlite3.connect(db_path) as conn:
        saved_date = conn.execute(
            "SELECT consultation_date FROM consultations WHERE id = ?",
            (payload["id"],),
        ).fetchone()[0]
    assert saved_date == "2024-02-29"


def test_create_consultation_accepts_tomorrow_with_tolerance(authenticated_client, consultation_payload):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    consultation_payload["consultation_date"] = tomorrow

    response = authenticated_client.post("/consultation", json=consultation_payload)

    assert response.status_code == 201
    assert response.json()["consultation_date"] == tomorrow


def test_create_consultation_rejects_future_date(authenticated_client, consultation_payload):
    consultation_payload["consultation_date"] = (date.today() + timedelta(days=2)).isoformat()

    response = authenticated_client.post("/consultation", json=consultation_payload)

    assert response.status_code == 422
    assert "later than tomorrow" in response.text


def test_create_consultation_rejects_invalid_date(authenticated_client, consultation_payload):
    consultation_payload["consultation_date"] = "2024-02-30"

    response = authenticated_client.post("/consultation", json=consultation_payload)

    assert response.status_code == 422


def test_create_consultation_rejects_more_than_ten_diagnoses(authenticated_client, consultation_payload):
    consultation_payload["diagnosis_codes"] = [
        "A00.0", "A00.1", "A00.9", "A01.00", "A01.01",
        "A01.02", "A01.03", "A01.04", "A01.05", "A01.09", "A01.1",
    ]

    response = authenticated_client.post("/consultation", json=consultation_payload)

    assert response.status_code == 422


def test_create_consultation_rejects_duplicate_diagnoses(authenticated_client, consultation_payload):
    consultation_payload["diagnosis_codes"] = ["A00.0", "a00.0"]

    response = authenticated_client.post("/consultation", json=consultation_payload)

    assert response.status_code == 422
    assert "must not contain duplicates" in response.text


def test_create_consultation_accepts_ten_diagnoses(authenticated_client, consultation_payload):
    consultation_payload["diagnosis_codes"] = [
        "A00.0", "A00.1", "A00.9", "A01.00", "A01.01",
        "A01.02", "A01.03", "A01.04", "A01.05", "A01.09",
    ]

    response = authenticated_client.post("/consultation", json=consultation_payload)

    assert response.status_code == 201
    assert len(response.json()["diagnoses"]) == 10
    assert response.json()["diagnoses"][0]["code"] == "A00.0"

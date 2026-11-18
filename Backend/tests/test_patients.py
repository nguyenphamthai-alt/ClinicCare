def test_search_patients_by_name(authenticated_client):
    response = authenticated_client.get("/patients?search=Nguyen")

    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert any("Nguyen" in item["full_name"] for item in payload)


def test_search_patients_returns_empty_list_when_no_matches(authenticated_client):
    response = authenticated_client.get("/patients?search=NoPatientNamedThis")

    assert response.status_code == 200
    assert response.json() == []


def test_create_patient(authenticated_client):
    response = authenticated_client.post(
        "/patients",
        json={
            "full_name": "Pham Test",
            "date_of_birth": "2001-03-15",
            "sex": "Male",
            "phone": "0905556677",
            "email": "pham.test@example.com",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["full_name"] == "Pham Test"
    assert payload["date_of_birth"] == "2001-03-15"
    assert payload["sex"] == "Male"


def test_create_patient_rejects_invalid_date(authenticated_client):
    response = authenticated_client.post(
        "/patients",
        json={
            "full_name": "Invalid Date Patient",
            "date_of_birth": "2025-02-30",
            "sex": "Female",
        },
    )

    assert response.status_code == 422


def test_invalid_patient_search_parameters_return_422(authenticated_client):
    response = authenticated_client.get("/patients?limit=0")

    assert response.status_code == 422

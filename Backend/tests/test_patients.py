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


def test_invalid_patient_search_parameters_return_422(authenticated_client):
    response = authenticated_client.get("/patients?limit=0")

    assert response.status_code == 422

def test_search_diagnosis_by_partial_code(authenticated_client):
    response = authenticated_client.get("/diagnosis?search=A00")

    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert any(item["code"].startswith("A00") for item in payload)


def test_search_diagnosis_returns_empty_list_when_no_matches(authenticated_client):
    response = authenticated_client.get("/diagnosis?search=NO_SUCH_CODE_123")

    assert response.status_code == 200
    assert response.json() == []


def test_empty_diagnosis_search_uses_existing_api_contract(authenticated_client):
    response = authenticated_client.get("/diagnosis?search=")

    assert response.status_code == 200
    assert response.json()


def test_invalid_diagnosis_search_parameters_return_422(authenticated_client):
    response = authenticated_client.get("/diagnosis?limit=0")

    assert response.status_code == 422

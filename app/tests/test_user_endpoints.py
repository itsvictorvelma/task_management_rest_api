from fastapi.testclient import TestClient


def test_create_user_returns_user_with_id(client: TestClient):
    response = client.post(
        "/signup", json={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "id" in json_data

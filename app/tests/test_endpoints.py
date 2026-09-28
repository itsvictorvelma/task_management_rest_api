from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_list_starts_empty(client: TestClient):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task_returns_task_with_id(client: TestClient):
    response = client.post("/tasks", json={"title": "Buy Milk", "description": "2%"})

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["title"] == "Buy Milk"
    assert json_data["completed"] is False
    assert "id" in json_data
    assert "created_at" in json_data


def test_get_missing_id_returns_404(client: TestClient):
    response = client.get("/tasks/1")

    assert response.status_code == 404


def test_patch_updates_only_completed(client: TestClient):
    created = client.post("/tasks", json={"title": "temp"}).json()
    task_id = created["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"completed": True})

    assert patch_response.status_code == 200
    json_data = patch_response.json()
    assert json_data["completed"] is True
    assert json_data["title"] == "temp"


def test_delete_returns_204_then_404(client: TestClient):
    created = client.post("/tasks", json={"title": "temp"}).json()
    task_id = created["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_list_respects_limit(client: TestClient):
    for i in range(20):
        client.post("/tasks", json={"title": f"task-{i}"})

    response = client.get("/tasks", params={"limit": 10})

    assert response.status_code == 200
    assert len(response.json()) == 10

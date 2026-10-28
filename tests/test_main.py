
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Task Tracker API is running"
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Learn Linux"
    assert tasks[1]["title"] == "Learn CI/CD"

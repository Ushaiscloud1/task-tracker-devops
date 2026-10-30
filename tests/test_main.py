
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
    # Create a task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Learn PostgreSQL",
            "completed": False
        }
    )

    assert create_response.status_code == 201

    created_task = create_response.json()

    # Retrieve all tasks
    response = client.get("/tasks")

    assert response.status_code == 200

    tasks = response.json()

    # Confirm the new task exists
    assert any(
        task["id"] == created_task["id"]
        for task in tasks
    )

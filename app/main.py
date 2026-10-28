
from fastapi import FastAPI

app = FastAPI(title="Task Tracker API")

tasks = [
    {"id": 1, "title": "Learn Linux", "completed": False},
    {"id": 2, "title": "Learn CI/CD", "completed": False},
]


@app.get("/")
def home():
    return {"message": "Task Tracker API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks")
def get_tasks():
    return tasks

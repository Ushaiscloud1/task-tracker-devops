
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.schemas import TaskCreate, TaskResponse

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Tracker API")


@app.get("/")
def home():
    return {"message": "Task Tracker API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task.title,
        completed=task.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.completed = updated_task.completed

    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

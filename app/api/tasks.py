from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import select
from schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from db.db import SessionDep
from db.models import Task

router = APIRouter()


def get_valid_task(task_id: int, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    return task


@router.post("/tasks", response_model=TaskResponse)
def create_task(task_in: TaskCreate, session: SessionDep):

    new_task = Task.model_validate(task_in)

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@router.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks(session: SessionDep, skip: int = 0, limit: int = 10):
    statement = select(Task).offset(skip).limit(limit)
    return session.exec(statement).all()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task: Task = Depends(get_valid_task)):
    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_update: TaskUpdate, session: SessionDep, task: Task = Depends(get_valid_task)
):
    update_data = task_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(session: SessionDep, task: Task = Depends(get_valid_task)):
    session.delete(task)
    session.commit()
    return None

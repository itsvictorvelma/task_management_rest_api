from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from db.db import SessionDep
from db.models import Task
from api.deps import get_valid_task

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/authTest")
async def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@router.post("/tasks", response_model=TaskResponse)
def create_task(task_in: TaskCreate, session: SessionDep):

    new_task = Task.model_validate(task_in)

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task

@router.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
):
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

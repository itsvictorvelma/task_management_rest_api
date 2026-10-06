from datetime import datetime
from pydantic import Field, BaseModel


class TaskBase(BaseModel):
    title: str = Field(max_length=50)
    description: str | None = Field(default=None, max_length=200)


class TaskCreate(BaseModel):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(None, max_length=50)
    description: str | None = Field(None, max_length=250)
    completed: bool | None = Field(default=None)


class TaskResponse(TaskBase):
    id: int
    completed: bool = Field(default=False)
    created_at: datetime

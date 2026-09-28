from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=50)
    description: str | None = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed: bool = Field(default=False)
    user_id: int | None = Field(default=None, foreign_key="user.id")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=20)
    password: str = Field(max_length=100)

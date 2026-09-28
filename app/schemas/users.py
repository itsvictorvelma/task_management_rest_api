from datetime import datetime

from pydantic import Field
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str = Field(max_length=50)
    password: str = Field(max_length=100)


class UserResponse(SQLModel):
    username: str = Field(max_length=50)


class UserUpdate(SQLModel):
    username: str | None = Field(max_length=50)
    password: str | None = Field(max_length=100)

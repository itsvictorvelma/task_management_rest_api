from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class userLogin(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

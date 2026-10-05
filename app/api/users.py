from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from db.db import SessionDep
from db.models import User
from schemas.users import UserCreate, UserResponse, UserUpdate
from core.security import hash_password
from api.deps import get_current_user

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def create_user(user_in: UserCreate, session: SessionDep):
    """Registers a new user with a hashed_password."""
    statement = select(User).where(User.username == user_in.username)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already registered",
        )

    hashed_pwd = hash_password(user_in.password)
    new_user = User(username=user_in.username, hashed_password=hashed_pwd)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.get("/me", response_model=UserResponse)
def get_currrent_user_profile(current_user: User = Depends(get_current_user)):
    """returns the authenticated caller's profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Updates the authenticated caller's details"""
    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(current_user, key, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user

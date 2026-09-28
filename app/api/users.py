from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from schemas.users import UserCreate, UserResponse, UserUpdate
from db.db import SessionDep
from db.models import User

router = APIRouter()


def get_valid_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="incorrect credentials and or they don't exist",
        )

    return user


@router.post("/signup", response_model=UserResponse)
def create_user(user_in: UserCreate, session: SessionDep):
    new_user = User.model_validate(user_in)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.get("/users", response_model=list[UserResponse])
def get_all_users(session: SessionDep):
    statement = select(User)
    return session.exec(statement).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user: User = Depends(get_valid_user)):
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_update: UserUpdate, session: SessionDep, user: User = Depends(get_valid_user)
):
    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(session: SessionDep, user: User = Depends(get_valid_user)):
    session.delete(user)
    session.commit()
    return None

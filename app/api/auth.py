from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from db.db import SessionDep
from db.models import User
from core.security import verify_password, create_access_token
from schemas.auth import Token

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(
    session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
):
    """Authenticates credentials and returns a signed JWT"""
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


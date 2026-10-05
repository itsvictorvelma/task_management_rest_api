from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from core.security import ALGORITHM, SECRET_KEY
from db.db import SessionDep
from db.models import User, Task
from schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
    """Extracts, decodes, and validates the jwt, reutning the database user object"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))

    except jwt.PyJWTError, ValueError:
        raise credentials_exception

    user = session.get(User, token_data.user_id)
    if user is None:
        raise credentials_exception

    return user


def get_valid_task(task_id: int, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    return task

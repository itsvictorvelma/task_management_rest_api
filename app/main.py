from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.db import create_db_and_tables, SessionDep

from api.tasks import router as tasks_router
from api.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def check_health():
    return {"message": "ok"}


app.include_router(tasks_router)
app.include_router(users_router)

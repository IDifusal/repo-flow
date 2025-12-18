from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy import text
from app.db import Base, engine, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Repo Flow Recipes API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

@app.get("/health/db")
def db_health_check(session=Depends(get_session)):
    session.execute(text("SELECT 1"))
    return {"database": "ok"}

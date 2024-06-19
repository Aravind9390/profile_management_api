# app/main.py
from fastapi import FastAPI
from app.routers import user
from app.database import engine
from app.models.user import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/api")

from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import notes, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Регистрируем роутеры
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])

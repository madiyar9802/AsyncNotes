from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import notes, tags

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Регистрируем роутеры
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["tags"])

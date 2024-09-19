from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import note_crud, tag_crud, models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
from typing import List


# API для заметок
@app.post("/api/v1/notes/", response_model=schemas.Note)
async def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return note_crud.create_note(db=db, note=note)


@app.get("/api/v1/notes/", response_model=List[schemas.Note])
async def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return note_crud.get_notes(db=db, skip=skip, limit=limit)


@app.get("/api/v1/notes/{note_id}", response_model=schemas.Note)
async def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = note_crud.get_note_by_id(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@app.put("/api/v1/notes/{note_id}", response_model=schemas.NoteUpdate)
async def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    return note_crud.update_note(db=db, note_id=note_id, note=note)


@app.delete("/api/v1/notes/{note_id}", response_model=schemas.Note)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    return note_crud.delete_note(db=db, note_id=note_id)


# API для тегов
@app.post("/api/v1/tags/", response_model=schemas.TagCreate)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return tag_crud.create_tag(db=db, tag=tag)


@app.get("/api/v1/tags/", response_model=List[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return tag_crud.get_tags(db=db, skip=skip, limit=limit)


@app.get("/api/v1/tags/{tag_id}", response_model=schemas.Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = tag_crud.get_tag_by_id(db=db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.put("/api/v1/tags/{tag_id}", response_model=schemas.Tag)
def update_tag(tag_id: int, name: str, db: Session = Depends(get_db)):
    tag = tag_crud.update_tag(db=db, tag_id=tag_id, name=name)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.delete("/api/v1/tags/{tag_id}", response_model=schemas.Tag)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = tag_crud.delete_tag(db=db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.crud import note_crud
from app.database import get_db
from typing import List

router = APIRouter()


# API для заметок
@router.post("/", response_model=schemas.Note)
async def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return note_crud.create_note(db=db, note=note)


@router.get("/", response_model=List[schemas.Note])
async def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return note_crud.get_notes(db=db, skip=skip, limit=limit)


@router.get("/{note_id}", response_model=schemas.Note)
async def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = note_crud.get_note_by_id(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@router.get("/tag/{tag_name}", response_model=List[schemas.Note])
async def read_notes_by_tag(tag_name: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    notes = note_crud.get_notes_by_tag(db=db, tag_name=tag_name, skip=skip, limit=limit)
    if not notes:
        raise HTTPException(status_code=404, detail="Notes with this tag not found")
    return notes


@router.put("/{note_id}", response_model=schemas.NoteUpdate)
async def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    return note_crud.update_note(db=db, note_id=note_id, note=note)


@router.delete("/{note_id}", response_model=schemas.Note)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    return note_crud.delete_note(db=db, note_id=note_id)

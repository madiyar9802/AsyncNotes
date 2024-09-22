from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas


def get_note_by_id_and_user(db: Session, note_id: int, user_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == user_id).first()


def get_notes(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).offset(skip).limit(limit).all()


def get_notes_by_tag(db: Session, user_id: int, tag_name: str, skip: int = 0, limit: int = 10):
    return db.query(models.Note).join(models.Note.tags).filter(
        models.Tag.name == tag_name,
        models.Note.owner_id == user_id).offset(skip).limit(limit).all()


def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(title=note.title, content=note.content, owner_id=user_id)
    db.add(db_note)

    for tag in note.tags:
        db_tag = db.query(models.Tag).filter(models.Tag.name == tag.name).first()
        if not db_tag:
            db_tag = models.Tag(name=tag.name)
        db_note.tags.append(db_tag)

    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(db: Session, note_id: int, user_id: int, note: schemas.NoteUpdate):
    db_note = get_note_by_id_and_user(db, note_id, user_id)
    if db_note:
        db_note.title = note.title
        db_note.content = note.content

        db_note.tags = []
        for tag in note.tags:
            db_tag = db.query(models.Tag).filter(models.Tag.name == tag.name).first()
            if not db_tag:
                db_tag = models.Tag(name=tag.name)
            db_note.tags.append(db_tag)

        db.commit()
        db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int, user_id: int):
    db_note = get_note_by_id_and_user(db, note_id, user_id)
    if db_note:
        db.delete(db_note)
        db.commit()
        return db_note
    else:
        raise HTTPException(status_code=404, detail="Note not found")

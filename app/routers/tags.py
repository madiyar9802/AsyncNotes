from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.crud import tag_crud
from app.database import get_db
from typing import List

router = APIRouter()


# API для тегов
@router.post("/", response_model=schemas.TagCreate)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return tag_crud.create_tag(db=db, tag=tag)


@router.get("/", response_model=List[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return tag_crud.get_tags(db=db, skip=skip, limit=limit)


@router.get("/{tag_id}", response_model=schemas.Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = tag_crud.get_tag_by_id(db=db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=schemas.Tag)
def update_tag(tag_id: int, name: str, db: Session = Depends(get_db)):
    tag = tag_crud.update_tag(db=db, tag_id=tag_id, name=name)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.delete("/{tag_id}", response_model=schemas.Tag)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = tag_crud.delete_tag(db=db, tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

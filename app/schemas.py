from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    title: str
    content: str
    tags: List[TagBase] = []


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    tags: List[Tag] = []

    class Config:
        orm_mode = True

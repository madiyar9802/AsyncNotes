from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Схемы для пользователя
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


# Схемы для токена
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Схемы для тегов
class TagBase(BaseModel):
    name: str


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


# Схемы для заметок
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

from pydantic import BaseModel
from typing import List

class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: str
    articles: List[ArticleOut]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str


class ArticleCreate(BaseModel):
    title: str
    content: str
    user_id: int

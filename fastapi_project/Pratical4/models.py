from typing import Optional
from sqlmodel import SQLModel,Field,Relationship
import uuid 

class User(SQLModel,table=True):
    # id:uuid.UUID =Field(default_factory=uuid.uuid4,primary_key=True)
    id: int | None = Field(default=None, primary_key=True)
    email:str = Field(index=True,unique=True)
    password:str
    bio:Optional[str]=None
    articles:list["Article"]=Relationship(back_populates="user")


class Article(SQLModel,table=True):
    id:int|None=Field(default=None, primary_key=True)
    user_id:int | None = Field(default=None,foreign_key="user.id")
    article_name:str=Field(index=True)
    user:User|None=Relationship(back_populates="articles")
    # user_id: int | None = Field(default=None, foreign_key="user.id")
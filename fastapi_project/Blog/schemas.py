from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str
    user_id:int
# This means:

# “I will only accept JSON that has:

# title → string

# body → string”



class showBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode=True

class User(BaseModel):
    name:str
    email:str
    password:str


class Login(BaseModel):
    email:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
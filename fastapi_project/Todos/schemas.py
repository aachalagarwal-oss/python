from pydantic import BaseModel


class todo(BaseModel):
    title:str
    completed:bool = False


class user(BaseModel):
    name:str
    email:str
    hashed_password:str

class show_todo(BaseModel):
    title:str
    completed:bool
    class Config():
        orm_mode=True



class update_todo(BaseModel):
    title:str
    completed:bool
    class Config():
        orm_mode=True

class response_todo(BaseModel):
    id:int
    title:str
    completed:bool
    class Config():
        orm_mode=True


class show_alltodos(BaseModel):
    id:int
    title:str
    completed:bool
    user_id:int

    class Config():
        orm_mode=True
    

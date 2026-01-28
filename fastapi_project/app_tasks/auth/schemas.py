from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TaskStatus(str,Enum):
    pending="pending"
    in_progress="in_progress"
    completed="completed"


class create_tasks(BaseModel):
    title:str
    description:str
    status:TaskStatus=TaskStatus.pending
    priority:int
    


class create_user(BaseModel):
    username:str
    password:str

class user_response(BaseModel):
    username:str


class create_subtasks(BaseModel):
    name:str
    is_done:bool=False
    priority:int

class TaskResponse(BaseModel):
    title:str
    description:str
    status: Optional[TaskStatus] = None
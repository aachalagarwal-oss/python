from fastapi import APIRouter,Depends,HTTPException
from app_tasks.db.database import get_db
from app_tasks.db import database
from app_tasks.auth import schemas
from app_tasks.db import models
from sqlalchemy.orm import Session
from typing import Annotated
from app_tasks.auth.routes import get_current_user

router=APIRouter(
    prefix="/tasks",
    tags=['tasks']
)

get_db=database.get_db

user_dependency=Annotated[dict,Depends(get_current_user)]


@router.post('/')
def create_tasks(user:user_dependency,request:schemas.create_tasks,db:Session=Depends(get_db)):
    tasks=models.Task(
        title=request.title,
        description=request.description,
        status=request.status,
        priority=request.priority,
        user_id=user["id"]
    )
    db.add(tasks)   
    db.commit()
    db.refresh(tasks)
    return tasks




@router.get('/')
def get_tasks(user:user_dependency,db:Session=Depends(get_db)):
    my_tasks=db.query(models.Task).filter(models.Task.user_id==user["id"]).all()

    if my_tasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no tasks found"
        )
    return my_tasks
    
    

@router.get('/{id}')
def get_tasks(id:int,user:user_dependency,db:Session=Depends(get_db)):
    my_tasks=db.query(models.Task).filter(models.Task.tasks_id==id).first()


    if my_tasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no tasks with id {id} found"
        )
    if(my_tasks.user_id!=user["id"]):
        raise HTTPException(
            status_code=404,
            detail=f"no tasks with  {id} found"
        )
    return my_tasks
    


@router.put('/{id}')
def update(id:int,user:user_dependency,request:schemas.create_tasks,db:Session=Depends(get_db)):
    my_tasks=db.query(models.Task).filter(models.Task.tasks_id==id).first()


    if my_tasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no tasks with id {id} found"
        )
    if(my_tasks.user_id!=user["id"]):
        raise HTTPException(
            status_code=404,
            detail=f"no tasks with  {id} found"
        )
    my_tasks.title=request.title
    my_tasks.description=request.description
    my_tasks.status=request.status
    my_tasks.priority=request.priority

    db.commit()
    db.refresh(my_tasks)
    return my_tasks




@router.delete('/{id}')
def update(id:int,user:user_dependency,request:schemas.create_tasks,db:Session=Depends(get_db)):
    my_tasks=db.query(models.Task).filter(models.Task.tasks_id==id).first()


    if my_tasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no tasks with id {id} found"
        )
    if(my_tasks.user_id!=user["id"]):
        raise HTTPException(
            status_code=404,
            detail=f"no tasks with  {id} found"
        )
    
    db.delete(my_tasks)
    db.commit()
    return 'The task is deleted'



@router.get('/{task_id}/summary')
def get_tasks(user:user_dependency,db:Session=Depends(get_db)):
    my_tasks=db.query(models.Task).filter(models.Task.user_id==user["id"]).all()

    if my_tasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no tasks found"
        )
    return my_tasks
    


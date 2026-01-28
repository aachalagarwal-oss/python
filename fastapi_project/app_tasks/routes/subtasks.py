from fastapi import APIRouter,Depends,HTTPException
from app_tasks.db import models
from app_tasks.auth import schemas
from sqlalchemy.orm import Session
from app_tasks.db.database import get_db
from typing import Annotated
from app_tasks.auth.routes import get_current_user
import redis
import json
from .tasks import redis_client
router=APIRouter(
    tags=['subtasks']
)

user_dependency=Annotated[dict,Depends(get_current_user)]

@router.post('/tasks/{task_id}/subtasks')
def create_subtasks(user:user_dependency,task_id:int,request:schemas.create_subtasks,db:Session=Depends(get_db)):
    get_subtasks= db.query(models.Task).filter(models.Task.tasks_id==task_id).first()

    if(get_subtasks.user_id!=user["id"]):
        raise HTTPException(
            status_code=404,
            detail=f" u r not allowed to make subtaks for someone else"
        )
    subtasks=models.subTasks(
        task_id=task_id,
        name=request.name,
        is_done=request.is_done,
        priority=request.priority
    )
    redis_client.delete(f"task_summary:{task_id}")
    db.add(subtasks)   
    db.commit()
    db.refresh(subtasks)
    return subtasks


@router.get('/tasks/{task_id}/subtasks')
def get_subtasks(user:user_dependency,task_id:int,db:Session=Depends(get_db)):
    my_tasks=db.query(models.Task).filter(models.Task.tasks_id==task_id).first()
    get_subtasks= db.query(models.subTasks).filter(models.subTasks.task_id==task_id).all()


    if get_subtasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no subtasks with tasks id {id} found"
        )
    if(my_tasks.user_id!=user["id"]):
        raise HTTPException(
            status_code=404,
            detail=f"not alowed to access someone else's tasks"
        )
    


    return get_subtasks


@router.put('/subTasks/{id}')
def create_subtasks(user:user_dependency,subtask_id:int,request:schemas.create_subtasks,db:Session=Depends(get_db)):
    get_subtasks= db.query(models.subTasks).filter(models.subTasks.subtasks_id==subtask_id).first()
    

    if get_subtasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no subtasks with tasks id {subtask_id} found"
        )
    get_tasks=db.query(models.Task).filter(models.Task.tasks_id==get_subtasks.task_id).first()

    if(get_tasks.user_id!=user["id"]):
        raise HTTPException(
            status_code=404,
            detail=f" u r not allowed to update subtaks for someone else"
        )
    


    
    get_subtasks.task_id=get_tasks.tasks_id
    get_subtasks.name=request.name
    get_subtasks.is_done=request.is_done
    get_subtasks.priority=request.priority 
    redis_client.delete(f"task_summary:{get_subtasks.task_id}")
    db.commit()
    db.refresh(get_subtasks)
    return get_subtasks


@router.delete('/subtasks/{id} ')
def delete(user:user_dependency,subtask_id:int,db:Session=Depends(get_db)):
    subtasks=db.query(models.subTasks).filter(
       models.subTasks.subtasks_id==subtask_id,   
   ).first()
   


    if subtasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no subtasks with tasks id {subtask_id} found"
        )
    get_tasks=db.query(models.Task).filter(models.Task.tasks_id==subtasks.task_id).first()

    if(get_tasks.user_id!=user["id"]):
        raise HTTPException(
            status_code=404,
            detail=f" u r not allowed to delete subtasks for someone else"
        )

    redis_client.delete(f"task_summary:{subtasks.task_id}")
    db.delete(subtasks)
    db.commit()
    return 'task deleted'



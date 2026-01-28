from fastapi import APIRouter,Depends,HTTPException
from app_tasks.db.database import get_db
from app_tasks.db import database
from app_tasks.auth import schemas
from app_tasks.db import models
from sqlalchemy.orm import Session
from typing import Annotated
from app_tasks.auth.routes import get_current_user
import redis
import json
from time import perf_counter
from typing import Optional,List
from app_tasks.db.models import Status
from app_tasks.auth.schemas import TaskResponse



router=APIRouter(
    prefix="/tasks",
    tags=['tasks']
)

get_db=database.get_db

user_dependency=Annotated[dict,Depends(get_current_user)]


# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)







@router.get('/{task_id}/summary')
def get_tasks_summary(task_id:int,user:user_dependency,db:Session=Depends(get_db)):

    cache_key = f"task_summary:{task_id}"

    s = perf_counter()
    #redis code
    cached_summary = redis_client.get(cache_key)
    if cached_summary:
       
        cache_data=json.loads(cached_summary.decode("utf-8"))
        e=perf_counter()
        print("Data from cache time",e-s)
        return cache_data


    
    my_tasks=db.query(models.Task).filter(models.Task.tasks_id==task_id).first()


    if my_tasks is None:
        raise HTTPException(
            status_code=404,
            detail=f"no tasks with id {task_id} found"
        )
    if(my_tasks.user_id!=user["id"]):
        raise HTTPException(
            status_code=404,
            detail=f"no sub_tasks with  {task_id} found"
        )
    

    sub_tasks=db.query(models.subTasks).filter(models.subTasks.task_id==task_id).count()

    completed_subtasks=db.query(models.subTasks).filter(models.subTasks.task_id==task_id,models.subTasks.is_done==True).count()

    pending_subtasks=sub_tasks-completed_subtasks
   
    response={
         

            "task_id": task_id, 

            "total_subtasks": sub_tasks, 

            "completed_subtasks": completed_subtasks, 

            "pending_subtasks": pending_subtasks

        
    }

    redis_client.setex(
        cache_key,
        40,
        json.dumps(response)
    )
  
#     json.dumps(response)
# Which becomes:
# "{\"task_id\":12,\"total_subtasks\":5,\"completed_subtasks\":2,\"pending_subtasks\":3}"
#becuase directly we cant store like as in form of dict
    data=response

    e = perf_counter()        
    print("Data from database time",e-s)
    return data
    


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




# @router.get('/')
# def get_tasks(user:user_dependency,db:Session=Depends(get_db),offset: int = 1, limit: int = 10):
    
#     my_tasks = db.query(models.Task).filter(models.Task.user_id == user["id"]).limit(limit).offset(offset).all()

#     if my_tasks is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"no tasks found"
#         )
    
#     return my_tasks
    

@router.get('/', response_model=List[TaskResponse])
def get_tasks(user:user_dependency,db:Session=Depends(get_db),offset: int = 1, limit: int = 10,status: Optional[Status] = None):

    query = db.query(models.Task).filter(models.Task.user_id == user["id"])
    
   
    if status:
        query = query.filter(models.Task.status == status.value)


    my_tasks = query.limit(limit).offset(offset).all()
    return my_tasks



@router.get('/{id}')
def get_tasks(id:int,user:user_dependency,db:Session=Depends(get_db)):
   
    my_tasks=db.query(models.Task).filter(models.Task.tasks_id==id).first()

    sub_tasks=db.query(models.subTasks).filter(models.subTasks.task_id==id).count()

    completed_subtasks=db.query(models.subTasks).filter(models.subTasks.task_id==id,models.subTasks.is_done==True).count()


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

    sub_tasks=db.query(models.subTasks).filter(models.subTasks.task_id==id).count()

    completed_subtasks=db.query(models.subTasks).filter(models.subTasks.task_id==id,models.subTasks.is_done==True).count()

    if(sub_tasks==completed_subtasks):
        my_tasks.status="completed"

    
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
def update(id:int,user:user_dependency,db:Session=Depends(get_db)):
    
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



 


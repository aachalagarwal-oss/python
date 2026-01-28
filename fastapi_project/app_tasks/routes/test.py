from app_tasks.db.database import SessionLocal
from app_tasks.db import models
import random
from fastapi import APIRouter,Depends,HTTPException
from app_tasks.db.database import get_db
from app_tasks.db import database
from app_tasks.auth import schemas
from app_tasks.db import models
from sqlalchemy.orm import Session
from typing import Annotated
from app_tasks.auth.routes import get_current_user


db = SessionLocal()


router=APIRouter(
    prefix="/test",
    tags=['test']
)

get_db=database.get_db

user_dependency=Annotated[dict,Depends(get_current_user)]


USER_ID = 8          
TASKS = 1000
SUBTASKS_PER_TASK = 50


@router.post('/')
def create_tasks(db:Session=Depends(get_db)):
    for t in range(TASKS):
        task = models.Task(
            title=f"Task {t}",
            description="load test",
            status="in_progress",
            priority=5,
            user_id=USER_ID
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        for s in range(SUBTASKS_PER_TASK):
            sub = models.subTasks(
                task_id=task.tasks_id,
                name=f"Sub {s}",
                is_done=random.choice([True, False])
            )
            db.add(sub)

        db.commit
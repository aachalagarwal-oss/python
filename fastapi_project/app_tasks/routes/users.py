from fastapi import APIRouter,Depends,HTTPException
from app_tasks.db.database import get_db
from sqlalchemy.orm import Session
from app_tasks.db import models
from app_tasks.auth import schemas
from app_tasks.auth import utils
from app_tasks.auth.utils import Hash
from app_tasks.auth import routes
from datetime import datetime, timedelta
from pydantic import BaseModel

router=APIRouter(
    prefix="/users",
    tags=['users']
)


class Token(BaseModel):
    access_token:str
    token_type:str



@router.post('/users',response_model=schemas.user_response)
def create_users(request:schemas.create_user,db:Session=Depends(get_db)):


    #calling the hashing file

   

    hashed_password=utils.Hash.hashit(request.password)
    user=models.User(
        username=request.username,
        password_hashed=hashed_password
    )

    if(db.query(models.User).filter(models.User.username == user.username).first()):
        raise HTTPException(
            status_code=404,
            detail=f"The user already exists"
        )
    

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
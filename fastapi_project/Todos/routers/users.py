from fastapi import APIRouter,Depends,HTTPException,status,BackgroundTasks
from .. import schemas,database,models
from sqlalchemy.orm import Session
from .. database import get_db
from passlib.context import CryptContext
from ..Hashing import Hash
from typing import Annotated
from ..auth import get_current_user

from ..email.service import send_email_notification

router=APIRouter()




get_db=database.get_db


router=APIRouter(
    prefix="/user",
    tags=['users']
)

@router.post('/')
def create_user(request:schemas.user, background_tasks: BackgroundTasks,  db: Session = Depends(get_db)  ):

    #hash the password
    hashed_password = Hash.bcrypt(request.hashed_password)


    user = models.Users(
        name=request.name,
        email=request.email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)


    # fire-and-forget email
    background_tasks.add_task(
        send_email_notification,
        user.email,                     # comes from request ke andar db ke andar object se
        f"Welcome {user.name}! "
    )
    return user
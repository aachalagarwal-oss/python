from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,database,models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..repository import user


router=APIRouter()



get_db=database.get_db

#hashing

# pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")


router=APIRouter(
    prefix="/user",
    tags=['users']
)

@router.post('/')
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    return user.create(request,db)
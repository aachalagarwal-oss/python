from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,database,models
from sqlalchemy.orm import Session
router=APIRouter()
get_db=database.get_db


@router.post('/user',tags=['users'])
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashedpassword=pwd_cxt.hash(request.password)
    user=models.Users(name=request.name,email=request.email,password=hashedpassword)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

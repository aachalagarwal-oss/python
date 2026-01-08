from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from ..import schemas
from ..import database,models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..Hashing import Hash
from datetime import datetime, timedelta, timezone
from . import token


router=APIRouter()

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post('/user',tags=['login'])
def login(request:schemas.Login,db: Session = Depends(database.get_db)):
    user=db.query(models.Users).filter(models.Users.email==request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Invalid credentials')
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Invalid credentials')
        
 
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token":access_token, "token_type":"bearer"}
                                                                      
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
# from pwdlib import PasswordHash
from pydantic import BaseModel
from . database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . models import Users
from jose import JWTError, jwt


router=APIRouter(
    prefix='/auth',
    tags=['auth']
)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')
# --auth is this file specifically while token is an endpoint


class createuserRequest(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]


# user created

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:createuserRequest):
    create_user_request=Users(
        email=create_user_request.email,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_request)
    db.commit()



#This function handles USER LOGIN and ISSUES a JWT token.
@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=authenticate_user(form_data.username,form_data.password,db)
    # username is by default it doesnt take email or such
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
    token=create_access_token(user.email,user.id,timedelta(minutes=20))
    return {
        "access_token": token,
        "token_type": "bearer"
    }

#user exists and password match
def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.email==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

#creates  a token 
def create_access_token(email:str,user_id:int,expires_time=timedelta):
    encode={'sub':email,'id':user_id}
    expires=datetime.now()+expires_time
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

#validating the token on every request
async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str=payload.get('sub')
        user_id:int=payload.get('id')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
        return {'email':email,'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user.')




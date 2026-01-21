from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pwdlib import PasswordHash
from pydantic import BaseModel
from . database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . models import Users
from jose import JWTError, jwt
from .config import settings
from .database import get_db
from . import database
from .Hashing import pwd_cxt



router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')
#--auth is this file specifically while token is an endpoint

class createuserRequest(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str
    

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    user_made_here=authenticate_user(form_data.username,form_data.password,db)
    if not user_made_here:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
    token=create_access_token(user_made_here.name,user_made_here.id,timedelta(minutes=20))
    # user = row from database
    return{
        "access_token":token,
        "token_type":"bearer"
    }

# 2...response_model=Token
# response_model = Token


# This tells FastAPI:

# “Whatever I return, it must look like this”

# class Token(BaseModel):
#     access_token: str
#     token_type: str



# What OAuth2PasswordRequestForm does

# It tells FastAPI:

# “Read username & password from form-data”

# Specifically:

# username

# password

# grant_type


# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     db: db_dependency
# ):
# This means:

# “FastAPI, please:

# Read the incoming request

# Extract username & password from form-data

# Put them into an object called form_data

# Give it to my function”



# scope
def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.name==username).first()
    if not user:
        return False
    if not pwd_cxt.verify(password,user.hashed_password):
        return False
    return user




# create_user_request: createuserRequest

# This means:

# Client must send JSON body

# JSON must match this model:

# {
#   "username": "aachal",
#   "password": "1234"
# }



def create_access_token(username:str,user_id:int,expires_time:timedelta):
    encode={'sub':username,'id':user_id}
    expires=datetime.now()+expires_time
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)



async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
        return {'username':username,'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user.')
from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from app_tasks.db.database import get_db
from sqlalchemy.orm import Session
from app_tasks.db.models import User
from .utils import pwd_cxt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app_tasks.auth.config import settings



router=APIRouter(
    prefix='/login',
    tags=['auth']
)


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
#OAuth 2.0 is an authorization framework, while a Bearer Token is a type of access token often used within OAuth 2.0

oauth2_bearer=OAuth2PasswordBearer(tokenUrl="login")

# OAuth2PasswordBearer does not check the token or verify it against a database, 
# it only checks that the token is included in the request. The verification of the token is usually done in the dependency.
#The tokenUrl parameter tells the OAuth2PasswordBearer logic where the token can be gotten from. 


class RegisterRequest(BaseModel):
    name: str
    password: str


class createuserRequest(BaseModel):
    username:str 
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str



@router.post("/",response_model=Token)
def login_for_access_tokens(formdata:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    user=authenticate_user(formdata.username,formdata.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='credentials are not proper')
    
    token=create_access_token(user.username,user.user_id,timedelta(minutes=20))

    return{
        "access_token":token,
        "token_type":"bearer"
    }



def authenticate_user(username:str,password:str,db):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not pwd_cxt.verify(password,user.password_hashed):
        return False
    return user
    

def create_access_token(name:str,user_id:int,expires_time:timedelta):
    encode={'sub':name,'id':user_id}
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







#An access token is a broader term, and a bearer token is a specific kind of access token.

# Bearer Token: Bearer tokens are tokens that are passed in the Authorization header of an HTTP request to authenticate the user. 
# They are typically represented as a random string of characters. Bearer tokens are simple and easy to implement. However, 
# the main drawback is that they lack the ability to verify the actor who issued the token. This means anyone in possession of a valid 
# bearer token can access the protected resources without further verification.

# OAuth2 Authorization: OAuth2 is an authorization framework that allows applications to obtain limited access to a user's resources 
# without sharing their credentials. It involves three parties: the resource owner (user), the client application, and the authorization server. 
# OAuth2 utilizes access tokens for authorization. Unlike bearer tokens, access tokens issued by OAuth2 are associated with a specific client 
# application and user. This allows more granular control over access to resources, preventing unauthorized access
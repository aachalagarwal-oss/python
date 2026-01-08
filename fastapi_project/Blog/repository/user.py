from .. import schemas,database,models
from sqlalchemy.orm import Session
from passlib.context import CryptContext



#hashing

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

def create(request:schemas.User,db:Session):
    hashedpassword=pwd_cxt.hash(request.password)
    user=models.Users(name=request.name,email=request.email,password=hashedpassword)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


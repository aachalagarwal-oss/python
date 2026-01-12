from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from authentication.database import Base

class Users(Base):
    __tablename__='users'

    id=Column(Integer,primary_key=True,index=True)
    user_name=Column(String,unique=True)
    hashed_password=Column(String)



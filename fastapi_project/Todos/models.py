from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
from .database import Base
from sqlalchemy.orm import relationship



class Todo(Base):

    __tablename__ = "todo"   
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    completed = Column(Boolean)
    user_id=Column(Integer,ForeignKey('users.id'))



class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    hashed_password=Column(String)
    todo=relationship("Todo",backref="users")
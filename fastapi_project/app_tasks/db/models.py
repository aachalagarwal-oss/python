from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,Enum
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

from enum import Enum as Enum
from fastapi import Query
from sqlalchemy import Enum as SQLEnum          


class Status(str,Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class User(Base):
    __tablename__="user"
    user_id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    password_hashed=Column(String)
    task=relationship("Task",backref="user")


class Task(Base):
    __tablename__="task"
    __allow_unmapped__ = True
    tasks_id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    status = Column(String)
    priority=Column(Integer)
    user_id=Column(Integer,ForeignKey('user.user_id'))
    subTasks=relationship("subTasks",backref="Task")


class subTasks(Base):
    __tablename__="subTasks"
    subtasks_id=Column(Integer,primary_key=True,index=True)
    task_id=Column(Integer,ForeignKey('task.tasks_id'))
    name=Column(String)
    is_done= Column(Boolean)
    priority=Column(Integer)

@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
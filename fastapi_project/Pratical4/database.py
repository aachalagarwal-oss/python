from sqlmodel import SQLModel, create_engine,Session
from .models import User
from typing import Annotated
from fastapi import Depends
from sqlalchemy import event


DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def get_session():
    with Session(engine) as session:
        yield session

event.listen(engine, "connect", enable_sqlite_foreign_keys)



SessionDep = Annotated[Session, Depends(get_session)]
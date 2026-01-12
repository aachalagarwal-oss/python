from fastapi import FastAPI,Depends,HTTPException,status
from typing import Annotated
from . import models
from sqlalchemy.orm import Session
from.database import engine,SessionLocal
from. import auth
from . auth import get_current_user
app=FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]





@app.get("/profile",status_code=status.HTTP_200_OK)
async def user(user:user_dependency,db:db_dependency):
    return{
        'message':"Hello authenticated user"
    }
from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schemas
from . import models
from Blog.database import engine,SessionLocal
from sqlalchemy.orm import Session
from .database import engine,get_db
from passlib.context import CryptContext
from .routers import blog,user,authentication

app=FastAPI()

models.Base.metadata.create_all(bind=engine)



#router
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)





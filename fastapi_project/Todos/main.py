from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schemas
from . import models
from sqlalchemy.orm import Session
from .database import engine,get_db
from .routers import users,todos
# ,authentication
from . import auth
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

app=FastAPI()

models.Base.metadata.create_all(bind=engine)






app.include_router(auth.router)

app.include_router(users.router)
app.include_router(todos.router)





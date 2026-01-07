from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schemas
from . import models
from Blog.database import engine,SessionLocal
from sqlalchemy.orm import Session
from .database import engine,get_db
from passlib.context import CryptContext
from .routers import blog,user
#dependency for hashing
app=FastAPI()

models.Base.metadata.create_all(bind=engine)


#router
app.include_router(blog.router)
app.include_router(user.router)


#hashing

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")





# @app.put('/blog')
# def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
#     blog=db.query(models.Blog).filter(models.Blog.id==id)
#     blog.update(request)
#     db.commit()

#     return 'updated'

# not working because update requires a dict and we are passing a model




@app.post('/user',tags=['users'])
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashedpassword=pwd_cxt.hash(request.password)
    user=models.Users(name=request.name,email=request.email,password=hashedpassword)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user




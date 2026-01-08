from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..import models,schemas,database

def get_all(db:Session):
    blogs=db.query(models.Blog).all()
    return blogs

def create(request:schemas.Blog,db:Session):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

def delete(id,db:Session):
    blog=db.query(models.Blog).where(models.Blog.id==id)
    blog.delete()
    db.commit()


def update(id,request:schemas.Blog,db:Session):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blog.update(request.dict())

#    .dict() because:SQLAlchemy works with plain Python data (dicts),Pydantic works with Python objects (models).

    db.commit()
    return 'updated'

# without .dict()
# DELETE worked because it needs no data.
# UPDATE failed because it needs data — and you gave it the wrong kind.




# @app.put('/blog')
# def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
#     blog=db.query(models.Blog).filter(models.Blog.id==id)
#     blog.update(request)
#     db.commit()

#     return 'updated'

# not working because update requires a dict and we are passing a model



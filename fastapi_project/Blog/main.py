from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schemas
from . import models
from Blog.database import engine,SessionLocal
from sqlalchemy.orm import Session
app=FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_200_OK)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs



# blogs=db.query(models.Blog)---just a blueprint
# .all():executes the SQL query

# to get dynamic values

@app.get('/blog/{id}',status_code=200)
def show(id,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).where(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id{id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{'detail':f"Blog with the id{id} is not available"}
    return blog


@app.delete('/blog')
def delete(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).where(models.Blog.id==id)
    blog.delete()
    db.commit()
    return 'done'


# @app.put('/blog')
# def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
#     blog=db.query(models.Blog).filter(models.Blog.id==id)
#     blog.update(request)
#     db.commit()

#     return 'updated'

# not working because update requires a dict and we are passing a model


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
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







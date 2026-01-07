from fastapi import FastAPI,Depends,Response,status,HTTPException
from . import schemas
from . import models
from Blog.database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
#dependency for hashing
app=FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()




#hashing

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")



@app.post('/blog',status_code=status.HTTP_200_OK,tags=['blogs'])
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',tags=['blogs'])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs



# blogs=db.query(models.Blog)---just a blueprint
# .all():executes the SQL query

# to get dynamic values

@app.get('/blog/{id}', response_model=schemas.showBlog,tags=['blogs'])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if blog is None:
        raise HTTPException(
            status_code=404,
            detail=f"Blog with id {id} not found"
        )

    return blog
#how to just get title and body

@app.delete('/blog',tags=['blogs'])
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


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
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


@app.post('/user',tags=['users'])
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    hashedpassword=pwd_cxt.hash(request.password)
    user=models.Users(name=request.name,email=request.email,password=hashedpassword)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user




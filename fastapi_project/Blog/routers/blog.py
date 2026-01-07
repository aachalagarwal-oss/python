from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,database,models
from sqlalchemy.orm import Session
router=APIRouter()
get_db=database.get_db

@router.get('/blog',tags=['blogs'])
def all(db:Session=Depends(database.get_db)):
    blogs=db.query(models.Blog).all()
    return blogs




# blogs=db.query(models.Blog)---just a blueprint
# .all():executes the SQL query

# to get dynamic values




@router.get('/blog/{id}', response_model=schemas.showBlog,tags=['blogs'])
def show(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if blog is None:
        raise HTTPException(
            status_code=404,
            detail=f"Blog with id {id} not found"
        )

    return blog


@router.post('/blog',status_code=status.HTTP_200_OK,tags=['blogs'])
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
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



@router.delete('/blog',tags=['blogs'])
def delete(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).where(models.Blog.id==id)
    blog.delete()
    db.commit()
    return 'done'
from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,database,models
from sqlalchemy.orm import Session
from ..repository import blog
from ..repository import user

get_db=database.get_db

router=APIRouter(
    prefix="/blog",
    tags=['blog']
)


@router.get('/')
def all(db:Session=Depends(database.get_db)):
    return blog.get_all(db)
# blogs=db.query(models.Blog)---just a blueprint
# .all():executes the SQL query

# to get dynamic values

@router.get('/{id}', response_model=schemas.showBlog)
def show(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if blog is None:
        raise HTTPException(
            status_code=404,
            detail=f"Blog with id {id} not found"
        )

    return blog

@router.post('/',status_code=status.HTTP_200_OK)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    return blog.create(request,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
   return blog.update(id,request,db)

# without .dict()
# DELETE worked because it needs no data.
# UPDATE failed because it needs data — and you gave it the wrong kind.

@router.delete('/')
def delete(id:int,db:Session=Depends(get_db)):
    blog.delete(id,db)





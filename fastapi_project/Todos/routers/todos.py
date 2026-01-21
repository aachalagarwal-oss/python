from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from .. import schemas,database,models
from sqlalchemy.orm import Session
from .. database import get_db
# from passlib.context import CryptContext
# from ..repository import user


from typing import Annotated
from ..auth import get_current_user


router=APIRouter()



get_db=database.get_db


router=APIRouter(
    prefix="/todo",
    tags=['todos']
)


user_dependency=Annotated[dict,Depends(get_current_user)]


@router.post('/')
def create_todo(user_token_one:user_dependency,request:schemas.todo,db:Session=Depends(get_db)):
    todo = models.Todo(
        title=request.title,
        completed=request.completed,
        user_id=user_token_one["id"]
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo




@router.get('/todos', response_model=List[schemas.show_alltodos])
def show(user:user_dependency,db: Session = Depends(database.get_db)):
    Todos_list = db.query(models.Todo).filter(models.Todo.user_id == user["id"]).all()

    if Todos_list is None:
        raise HTTPException(
            status_code=404,
            detail=f"no todo list found"
        )

    return Todos_list

@router.get('/{todo_id}', response_model=schemas.show_todo)
def show(user:user_dependency,todo_id: int, db: Session = Depends(database.get_db)):
    
    Todos_list = db.query(models.Todo).filter(models.Todo.id== todo_id).first()

    if Todos_list is None:
        raise HTTPException(
            status_code=404,
            detail=f"Todos with user_id {todo_id} not found"
        )
    
    if(Todos_list.user_id==user["id"]):
        return Todos_list
    else:
        raise HTTPException(
            status_code=404,
            detail=f"u r not allowed to access someone else's todos"
        )
        
    


@router.put('/todos/{todo_id}',response_model=schemas.response_todo)
def update(user:user_dependency,todo_id:int,request:schemas.update_todo,db: Session = Depends(database.get_db)):
   todo=db.query(models.Todo).filter(
       models.Todo.id==todo_id,   
   ).first()

   todo.title=request.title
   todo.completed=request.completed

   db.commit()
   db.refresh(todo)
   return todo




# Request schema = what the client is allowed to SEND
# Response schema = what the server promises to RETURN




@router.delete('/todos/{todo_id}')
def delete(user:user_dependency,todo_id:int,db:Session=Depends(database.get_db)):
    todo=db.query(models.Todo).filter(
       models.Todo.id==todo_id,   
   ).first()
    db.delete(todo)
    db.commit()
    return 'todo deleted'




# Key difference (THIS is the core idea)
# Context	What SQLAlchemy expects	What you must use
# .filter()	    SQL expression	Model.field
# if / logic	Python value	instance.field
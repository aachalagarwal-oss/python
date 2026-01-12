from fastapi import FastAPI,Depends,HTTPException,status
from typing import Annotated
from . import models
from sqlalchemy.orm import Session
from authentication.database import engine,SessionLocal
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



#         What happens here

# For every request:

# Create DB session

# Give it to route

# Close it after request finishes

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


# db_dependency = Annotated[Session, Depends(get_db)]
# This is just a shortcut so you don’t repeat code.

# Instead of writing:

# python
# Copy code
# db: Session = Depends(get_db)


@app.get("/",status_code=status.HTTP_200_OK)
async def user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    return {'User':user}



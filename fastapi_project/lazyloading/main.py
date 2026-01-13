from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas
from .models import User, Article
from sqlalchemy import select
from sqlalchemy.orm import selectinload


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users_add", response_model=schemas.UserOut)
def add_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    user = User(email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/articles_add", response_model=schemas.ArticleOut)
def add_article(request: schemas.ArticleCreate, db: Session = Depends(get_db)):
    article = Article(**request.dict())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

#lazy loadiing
# @app.get("/users/{id}", response_model=schemas.UserOut)
# def get_user(id: int, session: Session = Depends(get_db)):
#     user = session.get(User, id)
#     return user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, session: Session = Depends(get_db)):
    stmt=(
        select(User)
        .options(selectinload(User.articles))
        .where(User.id==id)
    )

    user = session.execute(stmt).scalar_one_or_none()
    return user

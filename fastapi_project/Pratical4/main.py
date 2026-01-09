from fastapi import FastAPI
from .database import create_db_and_tables
from .database import SessionDep,Session
from .models import User,Article

app=FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/create_user/")
def get_session(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/create_article/")
def create_article(article:Article, session: SessionDep) -> Article:
    session.add(article)
    session.commit()
    session.refresh(article)
    return article


@app.get("/users/{user_id}")
def get_users_articles(user_id:int,session:SessionDep):
    user=session.get(User,user_id)
    result=[]
    for article in user.articles:
        result.append({
            "id":article.id,
            "title":article.article_name
        })
    return{
        "user-id":user_id,
        "articles":result
    }
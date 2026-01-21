from fastapi import FastAPI,Depends
from app_tasks.db import models
from app_tasks.db.database import engine
from .routes import tasks,users,subtasks
from app_tasks.auth import routes

app=FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(subtasks.router)
app.include_router(routes.router)
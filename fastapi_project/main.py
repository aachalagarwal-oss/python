from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]

@app.post('/blog')
def create_blog(request:Blog):
    return{f'{request.title} Block is created with{request.body}'}










# @app.get("/blog?limit=10&published=true")
# def index():
#     return {"data": "Blog list"}


# @app.get('/blog')
# def index(limit=10,published:bool=True,sort: Optional[str]=None):
#     if published:
#         return (f"{limit} published blogs are shown")
#     else:
#         return(f"{limit} blogs are shown")

# @app.get('/blog/unpublished')
# def unpublished():
#     return{'data':'all unpublished blogs'}

# @app.get('/blog/{id}')
# def show(id:int):
#     return {'data':id}

# @app.get('/about')
# def about():
#     return {'data':['about page']}

# @app.get('/blog/{id}/comments')
# def comments(id):
#     return {'data':{'1','2'}}





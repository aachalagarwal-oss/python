from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel,Field
app=FastAPI()

class product(BaseModel):
    name:str
    price:float=Field(gt=0)
    category:Optional[str]=None


@app.post('/products' )
def accept_product(request:product):
    if request.category:
        category = request.category.strip()
    else:
        category = None
    msg= f"{request.name} is of Rs.{request.price} "


    if category:
        msg+=f"and a category{category}"



    return msg

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app=FastAPI()


@app.get('/items/{item_id}')
def get_item(item_id:int):
    return (f"{item_id}")


@app.get('/items')
def get_items(category=None,limit=10):
    return {f"Items has a category{category} and limit is {limit}"}

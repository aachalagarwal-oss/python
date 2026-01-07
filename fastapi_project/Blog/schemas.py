from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str
# This means:

# “I will only accept JSON that has:

# title → string

# body → string”
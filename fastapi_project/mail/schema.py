from pydantic import EmailStr, BaseModel
from typing import List

class Emailschema(BaseModel):
    email:List[EmailStr]
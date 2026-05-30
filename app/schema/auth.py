from pydantic import EmailStr, BaseModel
from typing import Union

class UserInCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserOutput(BaseModel):
    id:int
    name:str
    email:EmailStr
    token:str

class UserInUpdate(BaseModel):
    id:int
    name: str|None =None
    email:EmailStr|None=None
    password:str|None=None

class UserInLogin(BaseModel):
    email:EmailStr
    password:str

class UserWithToken(BaseModel):
    token:str
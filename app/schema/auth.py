from pydantic import EmailStr, BaseModel
from app.schema.user import User

class UserInCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserOutput(BaseModel):
    access_token:str
    refresh_token:str|None
    user:User

class UserInUpdate(BaseModel):
    id:int
    name: str|None =None
    email:EmailStr|None=None
    password:str|None=None

class UserInLogin(BaseModel):
    email:EmailStr
    password:str

class UserRefreshToken(BaseModel):
    refresh_token:str

class ChangePassword(BaseModel):
    current_password:str
    new_password:str
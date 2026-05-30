from fastapi import APIRouter
from app.schema.auth import UserInCreate,UserInLogin,UserOutput,UserWithToken
from app.service.user_service import UserService

authRouter=APIRouter()

@authRouter.post("/login",status_code=200,response_model=UserWithToken)
def login(loginDetails:UserInLogin):
    try:
      return UserService().login(userInput=loginDetails)
    except Exception as error:
      print(error)
      raise error
    
@authRouter.post("/signup",status_code=200,response_model=UserWithToken)
def signup(signupDetails:UserInCreate):
    try:
      return UserService().create_user(userDetails=signupDetails)
    except Exception as error:
      print(error)
      raise error
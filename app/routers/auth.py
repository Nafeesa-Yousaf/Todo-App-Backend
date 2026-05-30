from fastapi import APIRouter
from app.schema.auth import UserInCreate,UserInLogin,UserOutput
from app.service.auth_service import AuthService

authRouter=APIRouter()

@authRouter.post("/login",status_code=200,response_model=UserOutput)
def login(loginDetails:UserInLogin):
    try:
      return AuthService().login(userInput=loginDetails)
    except Exception as error:
      raise error
    
@authRouter.post("/signup",status_code=200,response_model=UserOutput)
def signup(signupDetails:UserInCreate):
    try:
      return AuthService().sign_up(userDetails=signupDetails)
    except Exception as error:
      print(error)
      raise error
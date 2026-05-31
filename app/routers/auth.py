from fastapi import APIRouter,Depends
from app.schema.auth import UserInCreate,UserInLogin,UserOutput,ChangePassword
from app.service.auth_service import AuthService
from app.util.protect_route import get_current_user

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
    
@authRouter.post("/refresh-token",status_code=200,response_model=str)
def refresh_access_token(refresh_token:str):
   try:
      return AuthService().refresh_access_token(refresh_token)
   except Exception as error:
      raise error
   
@authRouter.post("/change-password",status_code=200)
def change_password(password:ChangePassword,current_user: UserOutput=Depends(get_current_user)):
   try:
      return AuthService().change_password(password=password,current_user=current_user)
   except Exception as error:
      raise error
   
@authRouter.get("/logout",status_code=200)
def logout(current_user: UserOutput=Depends(get_current_user)):
   try:
      return AuthService().logout(current_user=current_user)
   except Exception as error:
      raise error
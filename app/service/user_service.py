from app.repository.user_repo import UserRepository
from app.schema.auth import UserInCreate,UserInLogin,UserOutput,UserWithToken
from app.security.hash_handler import HashHandler
from app.security.auth_handler import AuthHandler
from fastapi import HTTPException
import logging

class UserService:
    def __init__(self):
        self._userRepository=UserRepository()
    
    def create_user(self,userDetails:UserInCreate)->str:
        if(self._userRepository.get_user_by_email(email=userDetails.email)):
            raise HTTPException(status_code=400,detail="This Email already exists")
        hashPassword=HashHandler.hash_password(plain_password=userDetails.password)
        userDetails.password=hashPassword
        user= self._userRepository.create_user(userDetails=userDetails)
        token=AuthHandler.sign_jwt(user_id=user[1])
        return UserWithToken(token=token)


    def login(self,userInput:UserInLogin)->str:
         if not (self._userRepository.get_user_by_email(email=userInput.email)):
             raise HTTPException(status_code=400,detail="This email doesn't exists. Please Signup First")
         user=self._userRepository.get_user_by_email(email=userInput.email)
         logging.info(user)
         if HashHandler.verify_password(plain_password=userInput.password,hash_password=user[3]):
             token=AuthHandler.sign_jwt(user_id=user[1])
             if token:
                 return UserWithToken(token=token)
             raise HTTPException(status_code=500,detail="Unable to process request.")
         else:
             raise HTTPException(status_code=400,detail="Incorrect Credentials")


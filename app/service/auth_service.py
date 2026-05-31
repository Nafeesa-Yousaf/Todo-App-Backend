from app.repository.user_repo import UserRepository
from app.repository.auth_repo import AuthRepository
from app.schema.auth import UserInCreate,UserInLogin,UserOutput,ChangePassword
from app.service.hash_service import HashService
from app.service.jwt_service import JwtService
from app.schema.user import User
from fastapi import HTTPException
import logging

class AuthService:
    def __init__(self):
        self._userRepository=UserRepository()
        self._authRepository=AuthRepository()
    def sign_up(self,userDetails:UserInCreate)->UserOutput:
        if(self._userRepository.get_user_by_email(email=userDetails.email)):
            raise HTTPException(status_code=400,detail="This Email already exists")
        hashPassword=HashService.hash_password(plain_password=userDetails.password)
        userDetails.password=hashPassword
        createdUser= self._userRepository.create_user(userDetails=userDetails)
        access_token=JwtService.create_access_token(user_id=createdUser[0])
        refresh_token=JwtService.create_refresh_token(user_id=createdUser[0],user_email=createdUser[2])
        refresh_token_hash=HashService.hash_string(refresh_token)                
        self._authRepository.update_auth_fields(user_id=createdUser[0],token_version="+1",refresh_token=refresh_token_hash)
        return UserOutput(
            access_token=access_token,
            refresh_token=refresh_token,
            user= User(
                id=createdUser[0],
                name=createdUser[1],
                email=createdUser[2]
            )
        )


    def login(self,userInput:UserInLogin)->UserOutput:
         if not (self._userRepository.get_user_by_email(email=userInput.email)):
             raise HTTPException(status_code=400,detail="This email doesn't exists. Please Signup First")
         createdUser=self._userRepository.get_user_by_email(email=userInput.email)
         if HashService.verify_password(plain_password=userInput.password,hash_password=createdUser[3]):
             token=JwtService.create_access_token(user_id=createdUser[0])
             if token:
                refresh_token=JwtService.create_refresh_token(user_id=createdUser[0],user_email=createdUser[2])
                refresh_token_hash=HashService.hash_string(refresh_token)
                self._authRepository.update_auth_fields(user_id=createdUser[0],token_version="+1",refresh_token=refresh_token_hash)
                return UserOutput(
                access_token=token,
                refresh_token=refresh_token,
                user= User(
                    id=createdUser[0],
                    name=createdUser[1],
                    email=createdUser[2]
                    )
                )
             raise HTTPException(status_code=500,detail="Unable to process request.")
         else:
             raise HTTPException(status_code=400,detail="Incorrect Credentials")
         
    def refresh_access_token(self,refresh_token:str)->str:
        user_id=JwtService.verify_refresh_token(refresh_token=refresh_token)
        if user_id:
            self._authRepository.update_auth_fields(user_id=user_id,token_version="+1",)
            return JwtService.create_access_token(user_id=user_id)
        
    def change_password(self,password:ChangePassword,current_user:UserOutput):
        user=self._userRepository.get_user_by_id(id=current_user.id)
        if HashService.verify_password(plain_password=password.current_password,hash_password=user[3]):
            hash_password=HashService.hash_password(plain_password=password.new_password)
            refresh_token=JwtService.create_refresh_token(user_id=user[0],user_email=user[2])
            refresh_token_hash=HashService.hash_string(refresh_token)
            access_token=JwtService.create_access_token(user_id=user[0])
            self._authRepository.update_auth_fields(user_id=user[0],password=hash_password,refresh_token=refresh_token_hash,token_version="+1")
            return {"message": "Password changed successfully","access_token":access_token,"refresh_token":refresh_token}
        else:
            raise HTTPException(status_code=401,detail="Incorrect Current Password")
   
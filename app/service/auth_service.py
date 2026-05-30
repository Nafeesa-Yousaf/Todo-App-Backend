from app.repository.user_repo import UserRepository
from app.repository.auth_repo import AuthRepository
from app.schema.auth import UserInCreate,UserInLogin,UserOutput
from app.service.hash_service import HashService
from app.service.jwt_service import JwtService
from app.schema.user import User
from fastapi import HTTPException

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
        self._authRepository.update_refresh_token(refresh_token=refresh_token,user_id=createdUser[0])
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
                self._authRepository.update_refresh_token(refresh_token=refresh_token,user_id=createdUser[0])
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

   
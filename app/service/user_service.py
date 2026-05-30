from app.repository.user_repo import UserRepository
from app.schema.user import User
from fastapi import HTTPException

class UserService:
    def __init__(self):
        self._userRepository=UserRepository()
    def get_user_by_id(self,user_id:int)->User:
        user=UserRepository().get_user_by_id(user_id)
        if user:
            return User(
                id=user[0],
                name=user[1],
                email=user[2]
            )
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
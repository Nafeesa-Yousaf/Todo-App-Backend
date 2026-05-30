from decouple import config
import jwt
import time
from fastapi import HTTPException,status

JWT_SECRET=config("JWT_SECRET")
JWT_ALGORITHM=config("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE=900 #15 minutes
REFRESH_TOKEN_EXPIRES=864000 #10 days

class JwtService:
    @staticmethod
    def create_access_token(user_id:int)->str:
        payload={
            'user_id':user_id,
            'expires':time.time() +ACCESS_TOKEN_EXPIRE
        }
        token= jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    def create_refresh_token(user_id:int,user_email:str)->str:
        payload={
            'user_id':user_id,
            'user_email':user_email,
            'expires':time.time() +REFRESH_TOKEN_EXPIRES
        }
        token= jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    def decode_jwt(jwt_token:str)->dict:
        try:
            decoded_token= jwt.decode(jwt_token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
            if decoded_token["expires"]>=time.time():
                return decoded_token  
            else:
                HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" Access Token Expired")
        except:
            print("unable to decode token")
            return None
        

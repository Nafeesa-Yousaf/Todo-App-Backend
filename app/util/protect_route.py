from fastapi import HTTPException,Header,status
from app.schema.auth import UserOutput
from app.service.jwt_service import JwtService
from app.service.user_service import UserService
import logging

AUTH_PREFIX="Bearer "

def get_current_user(authorization:str = Header(None)):
    auth_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authorization Credentials"
    )
    if not authorization:
        logging.error("Token not found")
        raise auth_exception
    if not authorization.startswith(AUTH_PREFIX):
        logging.error("No prefix")
        raise auth_exception
    payload=JwtService.decode_jwt(jwt_token=authorization[len(AUTH_PREFIX):])
    if payload and payload["user_id"]:
        try:
            user=UserService().get_user_by_id(payload["user_id"])
            if (user):
                if (user["token_version"]== payload["token_version"]):
                    return user["user"]
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Access Token")
        except Exception as error:
            raise error
    raise auth_exception


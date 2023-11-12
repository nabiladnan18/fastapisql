import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRATION_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({'exp': expire})

    return jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, os.environ["SECRET_KEY"], algorithms=[ALGORITHM])
        user_id: str = payload.get('user_id')

        if not user_id:
            raise credentials_exception

        return TokenData(id=user_id)

    except JWTError:
        raise credentials_exception


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Bearer'})

    return verify_access_token(token, credentials_exception)

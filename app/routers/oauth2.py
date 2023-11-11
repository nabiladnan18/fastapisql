import os
from datetime import datetime, timedelta

from jose import JWTError, jwt


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRATION_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=ALGORITHM)

    return encoded_jwt

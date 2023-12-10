import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models
from .schemas import TokenData
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRATION_MINUTES = os.environ["ACCESS_TOKEN_EXPIRATION_MINUTES"]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, os.environ["SECRET_KEY"], algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if not user_id:
            raise credentials_exception

        return TokenData(id=user_id)

    except JWTError:
        raise credentials_exception


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

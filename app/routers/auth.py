from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from ..schemas import Token
from ..oauth2 import create_access_token
from .. import models
from ..database import get_db
from ..utils import verify

router = APIRouter(tags=["Authentication"], prefix="/login")


@router.post("/", response_model=Token)
# def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    # This is the manual mode e.g. where we defined the UserLogin schema
    # user = db.query(models.User).filter(
    #     models.User.email == user_credentials.email).first()
    # This is where we are using the OAuth2PasswordRequestForm
    #####################################################################
    # This automatically captures `username` and `password`
    # Returns as a dict
    # We do not have to do that manually
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user or not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user_id": user.id})
    # access_token = 'sometoken'

    return {"access_token": access_token, "token_type": "bearer"}

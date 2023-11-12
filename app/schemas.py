from datetime import datetime

from pydantic import BaseModel, EmailStr


# Defining a pydantic model
# This creates a validation for data sent by the client side


class PostBase(BaseModel):
    title: str
    content: str | int
    published: bool = True
    # rating: Optional[int]=None # `Optional` module imported from typing not fastapi


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    # These three are inherited from the baseclass
    # title: str
    # content: str
    # published: bool
    id: int
    created_at: datetime

    """
    We add the `class Config` because we would use the ORM to return the data
    to show to the user, which will then be an ORM object and not a valid 
    `dict` type. By adding this we tell the the Pydantic model to read the
    data even if it is not a valid dict. This is needed for the response.
    """
    class Config:
        # orm_mode is renamed to by from_attributes in V2
        # orm_mode = True
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        from_attributes = True


# No longer needed as OAuth2RequestForm is being used
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

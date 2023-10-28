from pydantic import BaseModel

# Defining a pydantic model
# This creates a validation for data sent by the client side
class PostBase(BaseModel):
    title: str
    content: str | int
    published: bool=True
    # rating: Optional[int]=None # `Optional` module imported from typing not fastapi

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

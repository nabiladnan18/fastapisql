from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.PostResponse])
# If we add `schemas.PostResponse` as the `repsose_model`, it does not work because
# we are returning a list of posts, whereas the response model tries to fit that
# into the model for one single post as is defined in PostResponse 🤦‍♂️
# This is why need to import List[] from typing library
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    posts = db.query(models.Post).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(get_current_user)):
    # ALT: new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.email, current_user.id)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{post_id}', response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    fetched_post = db.query(models.Post).get(
        {"id": post_id})  # get finds via PK
    if not fetched_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post id: {post_id} not found."
        )

    return fetched_post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_to_be_deleted = db.query(models.Post).filter(
        models.Post.id == post_id).first()
    if not post_to_be_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post id: {post_id} not found."
        )

    post_to_be_deleted.delete(synchronize_session=False)
    db.commit()


@router.put('/{post_id}', response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_to_be_updated = post_query.first()
    if not post_to_be_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post id: {post_id} not found."
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()

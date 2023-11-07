from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix='/posts'
)


@router.get('/', response_model=List[schemas.PostResponse])
# If we add `schemas.PostResponse` as the `repsose_model`, it does not work because
# we are returning a list of posts, whereas the response model tries to fit that
# into the model for one single post as is defined in PostResponse 🤦‍♂️
# This is why need to import List[] from typing library
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # ALT: new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{post_id}', response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    fetched_post = db.query(models.Post).get(
        {"id": post_id})  # get finds via PK
    if not fetched_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post id: {post_id} not found."
        )

    return fetched_post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
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
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
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

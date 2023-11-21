from pyexpat import model
from typing import Annotated
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db
from ..oauth2 import get_current_user

CurrentUser = Annotated[schemas.UserResponse, Depends(get_current_user)]
GetDatabase = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/votes',
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, current_user: CurrentUser, db: GetDatabase):
    if not db.query(models.Post.id).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: {vote.post_id} not found'
        )

    vote_query = db\
        .query(models.Vote)\
        .filter(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id
        )
    fetched_vote = vote_query.first()

    if vote.vote_dir == 1:
        if fetched_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User: {current_user.email} already voted for post with id: {vote.post_id}'
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'Voted successfully'}

    if not fetched_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: {vote.post_id} not found'
        )
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {'message': 'Vote removed successfully'}

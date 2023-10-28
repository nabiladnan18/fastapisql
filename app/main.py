import os

from fastapi import FastAPI, status, HTTPException, Depends
import psycopg
from psycopg.rows import dict_row
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

# db connection
models.Base.metadata.create_all(bind=engine)
try:
    DB_CONN = psycopg.connect(f'\
                              dbname={os.environ["DB_NAME"]}\
                              user={os.environ["DB_USER"]}\
                              password={os.environ["DB_PASSWORD"]}\
                              host={os.environ["DB_HOST"]}',
                              row_factory=dict_row
    )
except Exception as error:
    print(f"Error: {error}")
    raise error
print("successful connection!")

# FastAPI app
app = FastAPI()
@app.get('/')
async def root():
    return {'message': f'Hello World! Hello from the {os.environ["DB_HOST"]}!'}

@app.get('/posts')
def get_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db)):
    # ALT: new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/posts/{post_id}')
def get_post(post_id: int, db: Session=Depends(get_db)):
    fetched_post = db.query(models.Post).get({"id":post_id}) # get finds via PK
    if not fetched_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post id: {post_id} not found."
        )
    return fetched_post

@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session=Depends(get_db)):
    post_to_be_deleted = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post_to_be_deleted:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with post id: {post_id} not found."
        )
    post_to_be_deleted.delete(synchronize_session=False)
    db.commit()

@app.put('/posts/{post_id}')
def update_post(post_id: int, post: schemas.PostUpdate, db: Session=Depends(get_db)):
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

@app.get('/sqlalchemy')
def test_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# For Debugging for now
# In future that's the ingress of the api server
# import uvicorn
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port='8000')

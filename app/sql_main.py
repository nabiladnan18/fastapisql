import os

from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row

# db connection
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

cursor = DB_CONN.cursor()

# Defining a pydantic model
# This creates a validation for data sent by the client side
class Post(BaseModel):
    title: str
    content: str | int
    published: bool=True
    # rating: Optional[int]=None # `Optional` module imported from typing not fastapi

#* Not needed now that we have a functioning database
# my_posts = [{'id':1, 'title': 'title of the post1', 'content': 'content of post1'},
#             {'id':2, 'title': 'favourite food', 'content': 'I like pizza!'}]

# def find_index(post_id):
#     for index, post in enumerate(my_posts):
#         if post['id'] == post_id:
#             return index


app = FastAPI()
@app.get('/')
async def root():
    return {'message': f'Hello World! Hello from the {os.environ["DB_HOST"]}!'}

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'data': posts}

#* After the Post class is created
#* Changed status code from 200 to 201
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""
        INSERT INTO 
            posts (title, content, published)
        VALUES 
            (%s, %s, %s)
        RETURNING
            *
        """, [post.title, post.content, post.published]
    )
    new_post = cursor.fetchone()
    DB_CONN.commit()
    return {'data': new_post}

@app.get('/posts/{post_id}')
def get_post(post_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", [str(post_id)])
    fetched_post = cursor.fetchone()
    if not fetched_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post id: {post_id} not found."
        )
    return {'data': fetched_post}

@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", [str(post_id)])
    to_be_deleted_post = cursor.fetchone()
    DB_CONN.commit()
    if not to_be_deleted_post:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with post id: {post_id} not found."
        )

@app.put('/posts/{post_id}')
def update_post(post_id: int, post: Post):
    cursor.execute("""
            UPDATE 
                posts
            SET
                title = %s, content = %s, published = %s
            WHERE 
                id = %s
            RETURNING 
                *
            """, [post.title, post.content, post.published, post_id]
    )
    updated_post = cursor.fetchone()
    DB_CONN.commit()
    if not updated_post:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with post id: {post_id} not found."
        )
    return {'data': updated_post}


# For Debugging for now
# In future that's the ingress of the api server
# import uvicorn
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port='8000')

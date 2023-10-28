from typing import Optional
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel



# Defining a pydantic model
# This creates a validation for data sent by the client side
class Post(BaseModel):
    title: str
    content: str | int
    published: bool=True
    rating: Optional[int]=None # `Optional` module imported from typing not fastapi

my_posts = [{'id':1, 'title': 'title of the post1', 'content': 'content of post1'},
            {'id':2, 'title': 'favourite food', 'content': 'I like pizza!'}]

def find_index(post_id):
    for index, post in enumerate(my_posts):
        if post['id'] == post_id:
            return index


app = FastAPI()
@app.get('/')
async def root():
    return {'message': 'Hello World!'}

@app.get('/posts')
def get_posts():
    return {'data': my_posts}

# @app.post('/createPosts')
# def create_posts(payload: dict=Body(...)):
#     print(payload)
#     return {'title': f'{payload["title"]}',
#             'content': f'{payload["content"]}'}

#* After the Post class is created
#* Changed status code from 200 to 201
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post)
    # print(post.title)
    # print(post.content)
    # print(post.published)
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 100000000000)
    my_posts.append(post_dict)
    # print(post_dict)
    # print(my_posts)
    return {'data': post_dict}

@app.get('/posts/{post_id}')
# def get_post(post_id: int, response: Response):
# Used to get the response of the fastapi server
# and convert to a sensible http error code
# replaced with HTTPExceptions
def get_post(post_id: int):
    index = find_index(post_id)
    if index:
        return {"post_detail": my_posts[index]}
    """Using the `status` module from `fastapi` package.
    In this situation, it is better to raise `exceptions` using `HTTPException`
    from `fastapi` as we have more control."""
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"Post with {post_id} not found"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with post id: {post_id} not found."
    )

@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    index = find_index(post_id)
    if index:
        my_posts.pop(index)
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with post id: {post_id} not found."
        )

@app.put('/posts/{post_id}')
def update_post(post_id: int, post: Post):
    index = find_index(post_id)
    if index:
        my_post = post.model_dump()
        my_post['id'] = post_id
        my_posts[index] = my_post
        return {'data': my_post}
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with post id: {post_id} not found."
    )


# For Debugging for now
# # In future that's the ingress of the api server
# import uvicorn
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port='8000')

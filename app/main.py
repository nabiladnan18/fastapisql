import os

from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, posts, users

# db connection
models.Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    return {'message': f'Hello World! Hello from the {os.environ["DB_HOST"]}!'}

# For Debugging for now
# In future that's the ingress of the api server
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port='8000')

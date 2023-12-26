"""
Fixtures in the conftest.py will be available to everything that is in the tests package. This is one of the reasons why different test modules do not need to import client and session individually.
"""
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db

from app.main import app
from app import models
from app.oauth2 import create_access_token

DB_CONNECTION_STRING = f"postgresql://postgres:letmein@localhost:{os.environ['TEST_DATABASE_PORT']}/{os.environ['TEST_DATABASE']}"

engine = create_engine(DB_CONNECTION_STRING)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
# by default the scope is function
# this means that the fixture is run every time for a new function
# options are function, module, class, package, session
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


# # Dependency``
# def override_get_db():
#     db = TestSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# app.dependency_overrides[get_db] = override_get_db


# @pytest.fixture
# def client():
#     # Run our code before we run our test
#     # Destroys tables before creating them from scratch
#     models.Base.metadata.drop_all(bind=engine)
#     # Creates the database tables using the Pydantic Models
#     models.Base.metadata.create_all(bind=engine)
#     yield TestClient(app)
#     # Run our code after our test finishes
#     # Teardown
#     # models.Base.metadata.drop_all(bind=engine)
#     # But we will move it up to `before` so that it destroys all data
#     # before we start testing anything. This is important because,
#     # if we pass `-x` flag with pytest so that it stops at failure,
#     # we could see the state of the database where it was at the point of failure,


# TODO: FIGURE OUT HOW TO USE ALEMBIC TO SETUP AND TEARDOWN FOR TESTS
# def client():
#     alembic_config = config.Config("alembic_test.ini")
#     command.downgrade(revision="c24058f693f6", config=alembic_config)
#     command.upgrade(revision="head", config=alembic_config)
#     yield TestClient(app)


@pytest.fixture
def test_user(client):  # noqa
    user_data = {"email": "hello@gmail.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):  # noqa
    user_data = {"email": "servus@gmail.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorised_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def create_test_posts(test_user, test_user2, session):
    post_data = [
        {"title": "Athens", "content": "Amazing ruins", "owner_id": test_user["id"]},
        {
            "title": "Corfu",
            "content": "Beaches and cheap food",
            "owner_id": test_user["id"],
        },
        {"title": "Gilli", "content": "Party!", "owner_id": test_user["id"]},
        {"title": "Bali", "content": "Party!", "owner_id": test_user2["id"]},
    ]

    posts_list = list(map(lambda post: models.Post(**post), post_data))

    session.add_all(posts_list)
    session.commit()
    posts = session.query(models.Post).all()

    return posts

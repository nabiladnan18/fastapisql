"""
Fixtures in the conftest.py will be available to everything that is in the tests package. This is one of the reasons why different test modules do not need to import client and session individually.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db

from app.main import app
from app import models


DB_CONNECTION_STRING = "postgresql://postgres:letmein@localhost:5433/fastapisql_test"

engine = create_engine(DB_CONNECTION_STRING)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
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


@pytest.fixture()
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
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorised_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

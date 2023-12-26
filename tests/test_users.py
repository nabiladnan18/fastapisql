import os
from jose import jwt
import pytest

from app import schemas


def test_root(client):  # noqa: F811
    response = client.get("/")
    # print(response.json().get("message"))
    assert response.json().get("message") == "Hello World! Hello from the docker yo yo!"
    assert response.status_code == 200


def test_create_user(client, test_user):  # noqa: F811
    response = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    # we need add a trailing `/` to the url
    # it is because, FastAPI redirects the request to /users/
    # /users returns 307 temporary redirect
    # /users/ returns the 201
    # which is why the test will fail if /users is the url
    # create a user and check the app logs
    assert response.status_code == 201
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "hello123@gmail.com"


def test_login_user(client, test_user):  # noqa: F811
    response = client.post(
        "/login/",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    # field for the login is USERNAME not EMAIL
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        algorithms=[os.environ["ALGORITHM"]],
        key=os.environ["SECRET_KEY"],
    )
    assert test_user["id"] == payload.get("user_id")
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@email.com", "password", 403),
        ("hello@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password", 422),
        ("hello@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, session, email, password, status_code):
    response = client.post("/login/", data={"username": email, "password": password})
    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid credentials"

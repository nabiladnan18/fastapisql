import pytest

from sqlalchemy.exc import NoResultFound

from app import models, schemas


def test_get_all_posts(authorised_client, create_test_posts):
    response = authorised_client.get("/posts/")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == len(create_test_posts)
    for post in posts:
        assert schemas.PostOut.model_validate(post)
        # ? validates each `post` from the response against PostOut pydantic model??
        # ? I STILL DONT KNOW WHY THIS TEST PASSES 🙈
        # ? The magic of trial and error I guess


def test_unauthorised_user_get_all_posts(client, create_test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorised_user_get_one_posts(client, create_test_posts):
    response = client.get(f"/posts/{create_test_posts[0].id}")
    # create_test_posts returns a list of sqlalchemy objects
    # slice to get one object and then dot-notation to access attributes
    assert response.status_code == 401


def test_get_one_post_not_exist(authorised_client, create_test_posts):
    response = authorised_client.get("/posts/9999999")
    assert response.status_code == 404


def test_get_one_post(authorised_client, create_test_posts):
    response = authorised_client.get(f"/posts/{create_test_posts[0].id}")
    post = response.json()
    assert response.status_code == 200
    assert schemas.PostOut.model_validate(post)
    assert post["Post"]["id"] == create_test_posts[0].id


@pytest.mark.parametrize(
    "title, content",
    [("awesome_title", "awesome_content"), ("spam", "eggs"), ("spam", "spam")],
)
def test_create_one_post(
    authorised_client, test_user, create_test_posts, title, content
):
    response = authorised_client.post(
        "/posts/", json={"title": title, "content": content}
    )
    created_post = response.json()
    assert response.status_code == 201
    assert schemas.PostResponse.model_validate(created_post)
    assert created_post["title"] == title
    assert created_post["content"] == content
    assert created_post["published"] is True
    assert created_post["owner_id"] == test_user["id"]


def test_unauthorised_create_one_post(client, test_user, create_test_posts):
    response = client.post(
        "/posts/", json={"title": "awesome_title", "content": "awesome_content"}
    )
    assert response.status_code == 401


def test_delete_post_successful(
    authorised_client, test_user, create_test_posts, session
):
    delete_post_id = create_test_posts[1].id
    response = authorised_client.delete(f"/posts/{delete_post_id}")
    assert response.status_code == 204
    with pytest.raises(NoResultFound):
        assert session.get_one(models.Post, delete_post_id) is False


def test_delete_nonexisting_post(authorised_client):
    response = authorised_client.delete("/posts/9999999")
    assert response.status_code == 404


def test_delete_not_your_post(authorised_client, create_test_posts):
    response = authorised_client.delete(f"/posts/{create_test_posts[3].id}")
    assert response.status_code == 401


def test_update_post(authorised_client, test_user, create_test_posts):
    response = authorised_client.put(
        f"/posts/{create_test_posts[0].id}",
        json={
            "title": "changed title",
            "content": "changed content",
            "id": create_test_posts[0].id,
        },
    )
    assert response.status_code == 200
    updated_post = response.json()
    assert schemas.PostResponse.model_validate(updated_post)
    assert updated_post["id"] == create_test_posts[0].id
    assert updated_post["title"] == create_test_posts[0].title
    assert updated_post["content"] == create_test_posts[0].content


def test_unauthorised_delete(client, create_test_posts):
    response = client.delete(f"/posts/{create_test_posts[3].id}")
    assert response.status_code == 401


def test_unauthorised_update(client, create_test_posts):
    response = client.put(
        f"/posts/{create_test_posts[3].id}",
        json={
            "title": "changed title",
            "content": "changed content",
            "id": create_test_posts[0].id,
        },
    )
    assert response.status_code == 401

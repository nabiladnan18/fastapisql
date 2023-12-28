import pytest

from app import models


@pytest.fixture
def test_vote(create_test_posts, session, test_user):
    vote = models.Vote(post_id=create_test_posts[0].id, user_id=test_user["id"])
    session.add(vote)
    session.commit()


def test_upvote(authorised_client, create_test_posts):
    response = authorised_client.post(
        "/votes/",
        json={
            "post_id": create_test_posts[3].id,
            "vote_dir": 1,
        },
    )
    assert response.status_code == 201


def test_upvote_twice(authorised_client, create_test_posts, test_vote):
    response = authorised_client.post(
        "/votes/",
        json={
            "post_id": create_test_posts[0].id,
            "vote_dir": 1,
        },
    )
    assert response.status_code == 409


def test_downvote(authorised_client, create_test_posts, test_vote):
    response = authorised_client.post(
        "/votes/",
        json={
            "post_id": create_test_posts[0].id,
            "vote_dir": 0,
        },
    )
    assert response.status_code == 201


def test_upvote_not_exists(authorised_client, create_test_posts, test_vote):
    response = authorised_client.post(
        "/votes/",
        json={
            "post_id": 80000,
            "vote_dir": 1,
        },
    )
    assert response.status_code == 404


def test_upvote_not_authenticated(client, create_test_posts, test_vote):
    response = client.post(
        "/votes/",
        json={
            "post_id": create_test_posts[0].id,
            "vote_dir": 1,
        },
    )
    assert response.status_code == 401

import pytest

from src.auth.security import get_password_hash
from tests.conftest import create_test_auth_headers_for_user


async def test_get_all_posts(client, create_posts_in_db):
    await create_posts_in_db()
    headers = create_test_auth_headers_for_user(100)
    response = client.get("/v1/posts", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 5
    first_post = response.json()[1]
    assert "id" in first_post
    assert "owner" in first_post
    assert "title" in first_post
    assert "like" in first_post
    assert "dislike" in first_post
    assert "likes_count" in first_post
    assert "dislike_count" in first_post

    response = client.get("/v1/posts")
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


async def test_get_post(client):
    headers = create_test_auth_headers_for_user(107)
    response = client.get("/v1/posts/201", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "owner" in response.json()
    assert "title" in response.json()
    assert "like" in response.json()
    assert "dislike" in response.json()
    assert "likes_count" in response.json()
    assert "dislike_count" in response.json()
    response = client.get(
        "/v1/posts/201",
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

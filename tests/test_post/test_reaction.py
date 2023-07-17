import pytest

from tests.conftest import create_test_auth_headers_for_user
from src.posts.redis import get_likes_count, get_dislikes_count


async def test_like(client, create_posts_in_db):
    headers = create_test_auth_headers_for_user(402)
    await create_posts_in_db(start_num=400, count=5)
    like_data = {"like": True}
    response = client.post("/v1/posts/401/like", headers=headers, json=like_data)
    assert response.status_code == 200
    dislike_count = await get_dislikes_count(401)
    likes_count = await get_likes_count(401)
    assert likes_count == 1
    assert dislike_count == 0

    response = client.post("/v1/posts/401/like", headers=headers, json=like_data)
    assert response.status_code == 200
    likes_count = await get_likes_count(401)
    dislike_count = await get_dislikes_count(401)
    assert likes_count == 0
    assert dislike_count == 0

    headers = create_test_auth_headers_for_user(401)
    response = client.post("/v1/posts/401/like", headers=headers, json=like_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

    response = client.post("/v1/posts/401/like", json=like_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


async def test_dislike(client, create_posts_in_db):
    headers = create_test_auth_headers_for_user(502)
    await create_posts_in_db(start_num=500, count=5)
    like_data = {"like": True}
    response = client.post("/v1/posts/501/dislike", headers=headers, json=like_data)
    assert response.status_code == 200
    dislike_count = await get_dislikes_count(501)
    likes_count = await get_likes_count(501)
    assert likes_count == 0
    assert dislike_count == 1

    response = client.post("/v1/posts/501/dislike", headers=headers, json=like_data)
    assert response.status_code == 200
    likes_count = await get_likes_count(501)
    dislike_count = await get_dislikes_count(501)
    assert likes_count == 0
    assert dislike_count == 0

    headers = create_test_auth_headers_for_user(501)
    response = client.post("/v1/posts/501/dislike", headers=headers, json=like_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

    response = client.post("/v1/posts/501/dislike", json=like_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

from src.auth.security import get_password_hash
from tests.conftest import create_test_auth_headers_for_user


async def test_create_post(client, create_user_in_database):
    post_data = {"title": "test_title", "content": "test_content"}
    user = {
        "id": 105,
        "email": "test_post@example.com",
        "username": "test_post",
        "hashed_password": get_password_hash("testpass1"),
    }
    await create_user_in_database(**user)
    headers = create_test_auth_headers_for_user(105)
    response = client.post("/v1/posts", json=post_data, headers=headers)
    assert response.status_code == 201
    assert "post_id" in response.json()

    response = client.post("/v1/posts", json=post_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

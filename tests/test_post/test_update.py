import pytest

from tests.conftest import create_test_auth_headers_for_user


async def test_update_post(client, create_posts_in_db):
    headers = create_test_auth_headers_for_user(351)
    await create_posts_in_db(start_num=350, count=2)
    update_data = {"title": "new_title", "content": "new_content"}
    response = client.patch("/v1/posts/351", headers=headers, json=update_data)

    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    assert response.json()["content"] == update_data["content"]

    response = client.patch("/v1/posts/351", json=update_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

    response = client.patch("/v1/posts/352", headers=headers, json=update_data)

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

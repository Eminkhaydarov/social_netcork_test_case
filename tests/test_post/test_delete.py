import pytest

from tests.conftest import create_test_auth_headers_for_user


async def test_delete_post(client, create_posts_in_db):
    headers = create_test_auth_headers_for_user(302)
    await create_posts_in_db(start_num=301, count=2)
    response = client.delete("/v1/posts/302", headers=headers)

    assert response.status_code == 204

    response = client.delete(
        "/v1/posts/302",
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

    response = client.delete("/v1/posts/303", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

from src.auth.security import get_password_hash
from tests.conftest import create_test_auth_headers_for_user


async def test_login_for_access_token(client, create_user_in_database):
    user = {
        "id": 10,
        "email": "test@example.com",
        "username": "test",
        "hashed_password": get_password_hash("testpass1"),
    }
    await create_user_in_database(**user)
    response = client.post(
        "/v1/users/tokens",
        data={"username": "test", "password": "testpass1", "grant_type": "password"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    response = client.post(
        "/v1/users/tokens",
        data={"username": "testtt", "password": "testpass1", "grant_type": "password"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username"

    response = client.post(
        "/v1/users/tokens",
        data={"username": "test", "password": "testpass12", "grant_type": "password"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"


async def test_get_me(client):
    user = {
        "id": 100,
        "email": "test@example.com",
        "username": "test",
        "hashed_password": get_password_hash("testpass1"),
    }
    headers = create_test_auth_headers_for_user(100)
    response = client.get("/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == user["email"]
    assert response.json()["username"] == user["username"]

    response = client.get(
        "/v1/users/me",
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

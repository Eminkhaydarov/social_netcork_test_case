import pytest

from sqlalchemy import select


async def test_create_user(client):
    user_data = {
        "email": "alex@alexmaccaw.com",
        "username": "testuser",
        "password": "testpassword",
    }

    response = client.post("v1/users", json=user_data)
    assert response.status_code == 201
    assert "email" in response.json()
    assert "username" in response.json()


async def test_create_user_username_exists(client):
    user_data = {
        "email": "devil8-1@yandex.ru",
        "username": "testuser",
        "password": "testpassword",
    }

    response = client.post("v1/users", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists."


async def test_create_user_email_exists(
    client,
):
    user_data = {
        "email": "alex@alexmaccaw.com",
        "username": "testusertwo",
        "password": "testpassword",
    }

    response = client.post("v1/users", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists."


async def test_create_user_not_valid_email(
    client,
):
    user_data = {
        "email": "test@example.com",
        "username": "testusertwo",
        "password": "testpassword",
    }
    response = client.post("v1/users", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == f"Email {user_data['email']} is not valid"


async def test_additional_data(client, get_user_from_database):
    user = await get_user_from_database("alex@alexmaccaw.com")
    user_from_db = dict(user[0])

    assert user_from_db["location"] == "San Francisco, CA, US"
    assert user_from_db["full_name"] == "Alex MacCaw"
    assert user_from_db["company"] == "Alex MacCaw"

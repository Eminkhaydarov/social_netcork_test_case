import pytest


@pytest.mark.asyncio
async def test_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

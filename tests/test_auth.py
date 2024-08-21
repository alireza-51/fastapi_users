# tests/test_auth.py
import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_login(client, test_user):
    response = client.post("api/token", data={"username": "testnewuser", "password": "wrongpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    response = client.post("api/token", data={"username": "testnewuser", "password": "hashedpassword"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

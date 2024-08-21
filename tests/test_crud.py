# tests/test_crud.py
import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_user(client, db_session):
    response = client.post("api/users/", json={"username": "brandnewuser", "password": "newpassword", "email": "brandnewemail@example.com"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "brandnewuser"

@pytest.mark.asyncio
async def test_get_user(client, auth_token):
    token = auth_token['token']
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("api/users/", headers=headers)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_update_user(client, auth_token, admin_token):
    user_token = auth_token['token']
    headers = {"Authorization": f"Bearer {user_token}"}

    admin_token_header = admin_token['token']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test user can update himself
    response = client.put(f"api/users/{auth_token['user'].id}", headers=headers, json={"username": "newuser", "password": "newpassword", "email": "newemailupdate@example.com"})
    assert response.status_code == status.HTTP_200_OK
    
    # Test admin can update any user
    response = client.put(f"/users/{auth_token['user'].id}", headers=admin_headers, json={"username": "newuser", "password": "newpassword", "email": "newemailforupdate@example.com"})
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_delete_user(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token['token']}"}
    response = client.delete(f"/users/{admin_token['user'].id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK

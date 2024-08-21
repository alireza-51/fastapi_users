# import pytest
# from fastapi import status

# @pytest.mark.asyncio
# async def test_read_root(client):
#     response = client.get("/")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {"message": "Welcome to the FastAPI application!"}

# @pytest.mark.asyncio
# async def test_create_user(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     response = client.post(
#         "/users/",
#         headers=headers,
#         json={"username": "testuser2", "password": "password123", "role": "User", "is_active": True}
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json()["username"] == "testuser2"

# @pytest.mark.asyncio
# async def test_read_users(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     response = client.get("/users/", headers=headers)
#     assert response.status_code == status.HTTP_200_OK
#     assert isinstance(response.json(), list)

# @pytest.mark.asyncio
# async def test_read_user(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     response = client.get("/users/1", headers=headers)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["username"] == "testuser"

# @pytest.mark.asyncio
# async def test_update_user(client, auth_token, admin_token):
#     # Regular user updating their own data
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     response = client.put(
#         "/users/1", headers=headers, json={"username": "testuser", "password": "newpassword123"}
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["username"] == "testuser"

#     # Admin updating any user
#     admin_headers = {"Authorization": f"Bearer {admin_token}"}
#     response = client.put(
#         "/users/1", headers=admin_headers, json={"username": "testuser", "password": "adminupdatedpassword"}
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["username"] == "testuser"

# @pytest.mark.asyncio
# async def test_delete_user(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     response = client.delete("/users/1", headers=headers)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["username"] == "testuser"

# @pytest.mark.asyncio
# async def test_access_control_for_delete_user(client, auth_token):
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     response = client.delete("/users/2", headers=headers)
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert response.json()["detail"] == "Not enough permissions"

# @pytest.mark.asyncio
# async def test_access_control_for_update_user(client, auth_token, admin_token):
#     # Regular user trying to update another user's data
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     response = client.put(
#         "/users/2", headers=headers, json={"username": "otheruser", "password": "newpassword"}
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert response.json()["detail"] == "Not enough permissions"

#     # Admin updating another user's data
#     admin_headers = {"Authorization": f"Bearer {admin_token}"}
#     response = client.put(
#         "/users/2", headers=admin_headers, json={"username": "otheruser", "password": "adminnewpassword"}
#     )
#     assert response.status_code == status.HTTP_200_OK

from builtins import str
import pytest
from urllib.parse import urlencode
from app.models.user_model import UserRole
from app.utils.nickname_gen import generate_nickname

@pytest.mark.asyncio
async def test_user_access(async_client, user_token, verified_user, admin_user, admin_token):
    user_headers = {"Authorization": f"Bearer {user_token}"}
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test creating a user
    user_data = {"nickname": generate_nickname(), "email": "test@example.com", "password": "sS#fdasrongPassword123!"}
    response = await async_client.post("/users/", json=user_data, headers=user_headers)
    assert response.status_code == 403  # Access denied for non-admins
    
    # Test retrieving a user (denied for regular users, allowed for admin)
    response = await async_client.get(f"/users/{verified_user.id}", headers=user_headers)
    assert response.status_code == 403  # Access denied for non-admins

    response = await async_client.get(f"/users/{admin_user.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

    # Test updating email (denied for regular users, allowed for admin)
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=user_headers)
    assert response.status_code == 403  # Access denied for non-admins

    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]

    # Test deleting a user
    delete_response = await async_client.delete(f"/users/{admin_user.id}", headers=admin_headers)
    assert delete_response.status_code == 204
    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=admin_headers)
    assert fetch_response.status_code == 404  # Confirm user deletion

    # Test creating a user with duplicate email
    duplicate_user_data = {"email": verified_user.email, "password": "AnotherPassword123!", "role": UserRole.ADMIN.name}
    response = await async_client.post("/register/", json=duplicate_user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

    # Test invalid email
    invalid_email_data = {"email": "notanemail", "password": "ValidPassword123!"}
    response = await async_client.post("/register/", json=invalid_email_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_login(async_client, verified_user, unverified_user, locked_user):
    # Test successful login
    form_data = {"username": verified_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data and data["token_type"] == "bearer"

    # Test user not found
    invalid_user_form_data = {"username": "nonexistent@here.edu", "password": "RandomPass123!"}
    response = await async_client.post("/login/", data=urlencode(invalid_user_form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

    # Test incorrect password
    incorrect_pass_form_data = {"username": verified_user.email, "password": "WrongPassword123!"}
    response = await async_client.post("/login/", data=urlencode(incorrect_pass_form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

    # Test unverified user
    unverified_form_data = {"username": unverified_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post("/login/", data=urlencode(unverified_form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

    # Test locked user
    locked_user_form_data = {"username": locked_user.email, "password": "MySuperPassword$1234"}
    response = await async_client.post("/login/", data=urlencode(locked_user_form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_user_profile_management(async_client, admin_user, admin_token):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test updating GitHub profile
    github_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    response = await async_client.put(f"/users/{admin_user.id}", json=github_data, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == github_data["github_profile_url"]

    # Test updating LinkedIn profile
    linkedin_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    response = await async_client.put(f"/users/{admin_user.id}", json=linkedin_data, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == linkedin_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_user_listing(async_client, admin_token, manager_token, user_token):
    # Test listing users as admin
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/", headers=admin_headers)
    assert response.status_code == 200
    assert 'items' in response.json()

    # Test listing users as manager
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    response = await async_client.get("/users/", headers=manager_headers)
    assert response.status_code == 200

    # Test listing users as regular user (unauthorized)
    user_headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get("/users/", headers=user_headers)
    assert response.status_code == 403


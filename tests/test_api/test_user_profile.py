import pytest
from httpx import AsyncClient
from uuid import UUID

@pytest.mark.asyncio
async def test_update_own_profile(async_client, verified_user, user_token):
    """Test that a user can update their own profile"""
    profile_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "bio": "My new bio"
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(
        f"/users/{verified_user.id}/profile",
        json=profile_data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"
    assert response.json()["last_name"] == "Name"
    assert response.json()["bio"] == "My new bio"

@pytest.mark.asyncio
async def test_update_other_profile_forbidden(async_client, verified_user, user_token):
    """Test that a user cannot update another user's profile"""
    other_user_id = UUID('00000000-0000-0000-0000-000000000000')
    profile_data = {"first_name": "Updated"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(
        f"/users/{other_user_id}/profile",
        json=profile_data,
        headers=headers
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_admin_update_professional_status(async_client, verified_user, admin_token):
    """Test that an admin can update a user's professional status"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{verified_user.id}/professional-status",
        params={"status": True},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["is_professional"] is True

@pytest.mark.asyncio
async def test_user_cannot_update_professional_status(async_client, verified_user, user_token):
    """Test that a regular user cannot update professional status"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(
        f"/users/{verified_user.id}/professional-status",
        params={"status": True},
        headers=headers
    )
    assert response.status_code == 403

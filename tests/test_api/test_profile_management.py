import pytest
from httpx import AsyncClient
from uuid import UUID

@pytest.mark.asyncio
async def test_profile_validation(async_client, verified_user, user_token):
    """Test profile field validation"""
    invalid_data = {
        "first_name": "A" * 101,  # Too long
        "email": "notanemail",    # Invalid email
        "github_profile_url": "notaurl"  # Invalid URL
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(
        f"/users/{verified_user.id}/profile",
        json=invalid_data,
        headers=headers
    )
    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_profile_partial_update(async_client, verified_user, user_token):
    """Test that partial updates work correctly"""
    update_data = {
        "bio": "New bio text"
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(
        f"/users/{verified_user.id}/profile",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["bio"] == "New bio text"
    # Other fields should remain unchanged
    assert response.json()["email"] == verified_user.email

@pytest.mark.asyncio
async def test_profile_urls(async_client, verified_user, user_token):
    """Test updating profile URLs"""
    update_data = {
        "github_profile_url": "https://github.com/testuser",
        "linkedin_profile_url": "https://linkedin.com/in/testuser",
        "profile_picture_url": "https://example.com/pic.jpg"
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(
        f"/users/{verified_user.id}/profile",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == update_data["github_profile_url"]
    assert response.json()["linkedin_profile_url"] == update_data["linkedin_profile_url"]
    assert response.json()["profile_picture_url"] == update_data["profile_picture_url"]

@pytest.mark.asyncio
async def test_professional_status_notification(async_client, verified_user, admin_token, email_service):
    """Test that notifications are sent when professional status is updated"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{verified_user.id}/professional-status",
        params={"status": True},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["is_professional"] is True
    # Verify email service was called
    assert email_service.send_user_email.called

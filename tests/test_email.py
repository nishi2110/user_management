import pytest
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager
from app.models.user_model import User

@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    await email_service.send_user_email(user_data, 'email_verification')
    # Manual verification in Mailtrap

@pytest.mark.asyncio
async def test_send_verification_email(email_service):
    user = User(
        id=1,
        first_name="Test",
        email="test@example.com",
        verification_token="abc123"
    )
    await email_service.send_verification_email(user)
    # Verify email delivery or mock behavior

@pytest.mark.asyncio
async def test_send_account_locked_email(email_service):
    user = User(
        id=3,
        first_name="Locked User",
        email="lockeduser@example.com"
    )
    await email_service.send_account_locked_email(user)
    # Verify email delivery or mock behavior


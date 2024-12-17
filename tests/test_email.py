import pytest
    
@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    email_service.send_email('email_verification', 'Blank subject', user_data)
    # Manual verification in Mailtrap

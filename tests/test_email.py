import pytest

from app.utils.tasks import send_user_email
from celery.result import AsyncResult
    
@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    email_service.send_email('email_verification', 'Blank subject', user_data)
    # Manual verification in Mailtrap

"""
NOTE test only works when docker environment is up
@pytest.mark.docker
def test_celery_task_execution():
    '''
    Test if the Celery task executes and returns the expected result.
    '''
    # Define test inputs
    subject = "Docker Test Email"
    html_content = "<p>This is a test email.</p>"
    user_email = "test-celery-docker@example.com"
    
    # Call the task
    result = send_user_email.delay(subject, html_content, user_email)

    # Inspect task events
    task_result = AsyncResult(result.id)
    task_result.wait(5)

    # Check the result
    assert task_result.status == "SUCCESS"
"""
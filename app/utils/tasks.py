from celery.utils.log import get_task_logger

import requests
import json

from settings.config import settings
from app.utils.celery import app

logger = get_task_logger(__name__)

@app.task
def send_user_email(subject: str, html_content: str, user_email: str):
    headers = {
        "Authorization": f"Bearer {settings.mailtrap_api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": {"email": f'{settings.smtp_useremail}', "name": "MyApp Notifications"},
        "to": [{"email": f'{user_email}', "name": "Recipient"}],
        "subject": subject,
        "html": html_content,
    }

    try:
        response = requests.post(settings.mailtrap_api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logger.info(f"Email sent successfully to {user_email}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send email: {e}")
        raise

from celery.utils.log import get_task_logger
from celery import Task

import requests
import json

from settings.config import settings
from app.utils.celery import app

logger = get_task_logger(__name__)

class EmailTask(Task):
    autoretry_for = (requests.exceptions.RequestException,)
    retry_kwargs = {'max_retries': 3, 'countdown': 5}  # Retry 3 times with a 5s delay after each failure

@app.task(bind=True, base=EmailTask)
def send_user_email(self, subject: str, html_content: str, user_email: str):
    headers = {
        "Authorization": f"Bearer {settings.mailtrap_api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": {"email": f'{settings.mailtrap_useremail}', "name": "MyApp Notifications"},
        "to": [{"email": f'{user_email}', "name": "Recipient"}],
        "subject": subject,
        "html": html_content,
    }

    try:
        response = requests.post(settings.mailtrap_api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logger.info(f"Email sent successfully to {user_email}")
        return {
            "status_code": response.status_code,
            "recipient": user_email,
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send email: {e}")
        raise Exception(e)

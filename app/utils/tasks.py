from app.utils.smtp_connection import smtp_client
from app.utils.celery import app

@app.task
def send_user_email(subject: str, html_content: str, user_email: str):
    smtp_client.send_email(subject, html_content, user_email)

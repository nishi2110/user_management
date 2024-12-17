from builtins import ValueError, dict, str

from app.utils.template_manager import EmailTemplateManager
from app.utils.tasks import send_user_email

class EmailService:
    def __init__(self):
        self.template_manager = EmailTemplateManager()

    def send_email(self, email_type: str, subject: str, user_data: dict):
        html_content = self.template_manager.render_template(email_type, **user_data)
        send_user_email.delay(subject, html_content, user_data['email'])

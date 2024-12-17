from builtins import ValueError, dict, str

from settings.config import settings
from app.utils.template_manager import TemplateManager
from app.models.user_model import User
from app.utils.tasks import send_user_email

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.template_manager = template_manager

    def send_user_email(self, user_data: dict, email_type: str):
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        html_content = self.template_manager.render_template(email_type, **user_data)
        send_user_email.delay(subject_map[email_type], html_content, user_data['email'])

    def send_verification_email(self, user: User):
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        self.send_user_email({
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }, 'email_verification')

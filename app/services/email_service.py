# email_service.py
import logging
from builtins import ValueError, dict, str
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        """
        Send an email to the user.

        Args:
            user_data (dict): Data required for email templates.
            email_type (str): Type of email to send.

        Raises:
            ValueError: If email_type is invalid.
        """
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            logger.error(f"Invalid email type provided: {email_type}")
            raise ValueError("Invalid email type")

        try:
            html_content = self.template_manager.render_template(email_type, **user_data)
            self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])
            logger.info(f"Email sent successfully to {user_data['email']} for {email_type}.")
        except Exception as e:
            logger.error(f"Failed to send email to {user_data['email']} for {email_type}: {e}")
            raise

    async def send_verification_email(self, user: User):
        """
        Send a verification email to the user.

        Args:
            user (User): The user object containing details for email.
        """
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        try:
            await self.send_user_email({
                "name": user.first_name,
                "verification_url": verification_url,
                "email": user.email
            }, 'email_verification')
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {e}")

    async def send_password_reset_email(self, user: User):
        """
        Send a password reset email to the user.

        Args:
            user (User): The user object containing details for email.
        """
        reset_url = f"{settings.server_base_url}reset-password/{user.id}/{user.reset_token}"
        try:
            await self.send_user_email({
                "name": user.first_name,
                "reset_url": reset_url,
                "email": user.email
            }, 'password_reset')
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {e}")

    async def send_account_locked_email(self, user: User):
        """
        Send an account locked notification email to the user.

        Args:
            user (User): The user object containing details for email.
        """
        try:
            await self.send_user_email({
                "name": user.first_name,
                "email": user.email
            }, 'account_locked')
        except Exception as e:
            logger.error(f"Failed to send account locked email to {user.email}: {e}")

from builtins import ValueError, dict, str
import logging
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        Send an email to the user based on the provided email type.

        Args:
            user_data (dict): User data required for the email.
            email_type (str): Type of email to send.

        Raises:
            ValueError: If the email type is invalid.
        """
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            logger.error(f"Invalid email type: {email_type}")
            raise ValueError("Invalid email type")

        logger.info(f"Rendering template for email type: {email_type}")
        html_content = self.template_manager.render_template(email_type, **user_data)

        logger.info(f"Sending email to: {user_data['email']}")
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User):
        """
        Send a verification email to the user.

        Args:
            user (User): The user object containing user details.
        """
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        logger.info(f"Generating verification email for user ID: {user.id}")
        await self.send_user_email({
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }, 'email_verification')

    async def send_password_reset_email(self, user: User):
        """
        Send a password reset email to the user.

        Args:
            user (User): The user object containing user details.
        """
        reset_url = f"{settings.server_base_url}reset-password/{user.id}/{user.reset_token}"
        logger.info(f"Generating password reset email for user ID: {user.id}")
        await self.send_user_email({
            "name": user.first_name,
            "reset_url": reset_url,
            "email": user.email
        }, 'password_reset')

    async def send_account_locked_email(self, user: User):
        """
        Send an account locked notification email to the user.

        Args:
            user (User): The user object containing user details.
        """
        logger.warning(f"Account locked for user ID: {user.id}")
        await self.send_user_email({
            "name": user.first_name,
            "email": user.email
        }, 'account_locked')

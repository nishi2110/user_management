from app.services.email_service import EmailService
from app.models.user_model import User, UserRole
from settings.config import settings

class NotificationService:
    email_service = EmailService()
    text_service = None # we can implement texting services by collecting the user's phone number

    @classmethod
    def email_verification(cls, user: User):
        subject = "Verify Your Account"
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        user_data = {
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }
        cls.email_service.send_email(email_type=cls.email_verification.__name__, subject=subject, user_data=user_data)
    
    @classmethod
    def account_locked(cls, user: User):
        subject = "Account Locked!"
        user_data = {
            "name": user.first_name,
            "failed_attempts": user.failed_login_attempts,
            "email": user.email
        }
        cls.email_service.send_email(email_type=cls.account_locked.__name__, subject=subject, user_data=user_data)
    
    @classmethod
    def account_unlocked(cls, user: User):
        subject = "Account Unlocked!"
        user_data = {
            "name": user.first_name,
            "email": user.email
        }
        cls.email_service.send_email(email_type=cls.account_unlocked.__name__, subject=subject, user_data=user_data)

    @classmethod
    def role_updated(cls, user: User, previous_role: str):
        subject = "Role Updated!"
        user_data = {
            "name": user.first_name,
            "email": user.email,
            "role": user.role,
            "previous_role": previous_role
        }
        cls.email_service.send_email(email_type=cls.role_updated.__name__, subject=subject, user_data=user_data)

    @classmethod
    def password_updated(cls, user: User):
        subject = "Password Updated!"
        user_data = {
            "name": user.first_name,
            "email": user.email,
        }
        cls.email_service.send_email(email_type=cls.password_updated.__name__, subject=subject, user_data=user_data)

    @classmethod
    def professional_status_updated(cls, user: User):
        subject = "Professional status updated"
        user_data = {
            "name": user.first_name,
            "email": user.email,
            "updated_at": user.professional_status_updated_at
        }
        cls.email_service.send_email(email_type=cls.professional_status_updated.__name__, subject=subject, user_data=user_data)

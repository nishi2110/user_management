from builtins import bool, str
from email_validator import validate_email, EmailNotValidError
import re

def validate_email_address(email: str) -> bool:
    """
    Validate the email address using the email-validator library.
    
    Args:
        email (str): Email address to validate.
    
    Returns:
        bool: True if the email is valid, otherwise False.
    """
    try:
        # Validate and get detailed info
        validate_email(email)
        return True
    except EmailNotValidError as e:
        # Email not valid, return False
        print(f"Invalid email: {e}")
        return False

def validate_url_safe_username(username: str) -> bool:
    """
    Validate if a username is URL-safe.
    
    Args:
        username (str): Username to validate.
    
    Returns:
        bool: True if the username is URL-safe, otherwise False.
    """
    # Regular expression for a URL-safe username (letters, numbers, hyphen, underscore)
    pattern = r'^[a-zA-Z0-9-_]+$'
    
    # Validate against the pattern
    if re.match(pattern, username):
        return True
    else:
        print(f"Invalid username: {username} is not URL-safe.")
        return False

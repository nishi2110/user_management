# app/services/jwt_service.py
from builtins import dict, str
import jwt
from datetime import datetime, timedelta
from settings.config import settings

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.

    Args:
        data (dict): Data to encode in the token.
        expires_delta (timedelta, optional): Expiration duration. Defaults to settings.access_token_expire_minutes.

    Returns:
        str: Encoded JWT.
    """
    to_encode = data.copy()
    if 'role' in to_encode:
        to_encode['role'] = to_encode['role'].upper()
    
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str):
    """
    Decode a JWT token and handle errors.

    Args:
        token (str): JWT token to decode.

    Returns:
        dict or None: Decoded token data if successful; None otherwise.
    """
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        print("Error: Token has expired.")
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        print("Error: Invalid token.")
        return {"error": "Invalid token"}
    except Exception as e:
        print(f"Unexpected error during token decoding: {e}")
        return {"error": "Unexpected error occurred"}

def is_token_expired(token: str):
    """
    Check if the provided token has expired.

    Args:
        token (str): JWT token to check.

    Returns:
        bool: True if token is expired, False otherwise.
    """
    decoded = decode_token(token)
    if decoded and "exp" in decoded:
        expiration_time = datetime.utcfromtimestamp(decoded["exp"])
        return datetime.utcnow() > expiration_time
    return True

def refresh_token(token: str):
    """
    Refresh an expired token by generating a new one with the same payload.

    Args:
        token (str): Expired JWT token to refresh.

    Returns:
        str or None: New token if refreshable; None otherwise.
    """
    decoded = decode_token(token)
    if decoded and "exp" in decoded:
        if is_token_expired(token):
            decoded.pop("exp", None)  # Remove old expiration
            return create_access_token(data=decoded)
    return None

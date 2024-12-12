from builtins import dict, str
from datetime import datetime, timedelta
import jwt
from settings.config import settings

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token with optional expiration time.

    Args:
        data (dict): Data to include in the token payload.
        expires_delta (timedelta, optional): Expiration duration of the token.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()

    # Ensure role is uppercase if present
    if 'role' in to_encode:
        to_encode['role'] = to_encode['role'].upper()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def decode_token(token: str):
    """
    Decode a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict or None: Decoded token payload if valid, None otherwise.
    """
    try:
        decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return decoded
    except jwt.PyJWTError:
        return None

def refresh_access_token(token: str):
    """
    Refresh an access token by generating a new token with updated expiration.

    Args:
        token (str): The JWT token to refresh.

    Returns:
        str or None: Refreshed JWT token if the input token is valid, None otherwise.
    """
    decoded = decode_token(token)
    if decoded:
        # Remove the "exp" field and create a new token
        decoded.pop("exp", None)
        return create_access_token(data=decoded)
    return None

def is_token_expired(token: str):
    """
    Check if a JWT token is expired.

    Args:
        token (str): The JWT token to check.

    Returns:
        bool: True if the token is expired, False otherwise.
    """
    decoded = decode_token(token)
    if decoded:
        exp = decoded.get("exp")
        if exp:
            return datetime.utcnow() > datetime.utcfromtimestamp(exp)
    return True

def extract_claim(token: str, claim: str):
    """
    Extract a specific claim from a JWT token.

    Args:
        token (str): The JWT token to extract the claim from.
        claim (str): The claim key to extract.

    Returns:
        Any: The value of the claim if it exists, None otherwise.
    """
    decoded = decode_token(token)
    if decoded:
        return decoded.get(claim)
    return None

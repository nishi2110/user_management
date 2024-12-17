from typing import AsyncGenerator
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db as database_get_db
from settings.config import Settings, settings
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import decode_token

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in database_get_db():
        yield session

def get_settings() -> Settings:
    return settings

def get_email_service() -> EmailService:
    template_manager = TemplateManager()
    return EmailService(template_manager=template_manager)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    user_role: str = payload.get("role")
    if user_id is None or user_role is None:
        raise credentials_exception
    return {"user_id": user_id, "role": user_role}

def require_role(role: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in role:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return current_user
    return role_checker

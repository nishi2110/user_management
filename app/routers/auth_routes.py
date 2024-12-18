from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_settings
from app.schemas.token_schema import TokenResponse
from app.services.jwt_service import create_access_token
from app.services.user_service import UserService

router = APIRouter()
settings = get_settings()

@router.post("/login/", response_model=TokenResponse, tags=["Authentication"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)
):
    """
    User login endpoint.
    Validates user credentials and generates an access token.
    """
    user = await UserService.login_user(session, form_data.username, form_data.password)
    if user:
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role.name}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect email or password")

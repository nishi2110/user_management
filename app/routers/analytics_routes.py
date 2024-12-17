from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, require_role
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/analytics/inactive-users", tags=["Analytics"])
async def get_inactive_users(
    period: str,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role(["ADMIN"]))
):
    period_map = {
        "24h": timedelta(hours=24),
        "48h": timedelta(hours=48),
        "1w": timedelta(weeks=1),
        "1y": timedelta(days=365)
    }
    
    if period not in period_map:
        raise HTTPException(status_code=400, detail="Invalid period")
        
    inactive_users = await AnalyticsService.get_inactive_users(db, period_map[period])
    return {"inactive_users": [user.id for user in inactive_users]}

@router.get("/analytics/conversion-rate", tags=["Analytics"])
async def get_conversion_rate(
    start_date: datetime,
    end_date: datetime,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role(["ADMIN"]))
):
    return await AnalyticsService.get_conversion_rate(db, start_date, end_date) 
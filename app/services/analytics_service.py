from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analytics_model import UserAnalytics
from app.models.user_model import User, UserRole
import uuid

class AnalyticsService:
    @staticmethod
    async def track_event(
        session: AsyncSession,
        event_type: str,
        session_id: str,
        user_id: Optional[uuid.UUID] = None,
        previous_role: Optional[UserRole] = None,
        new_role: Optional[UserRole] = None,
        metadata: Optional[str] = None
    ):
        try:
            analytics = UserAnalytics(
                user_id=user_id,
                session_id=session_id,
                event_type=event_type,
                previous_role=previous_role,
                new_role=new_role,
                event_metadata=metadata
            )
            session.add(analytics)
            await session.flush()
            await session.commit()
            await session.refresh(analytics)
            return analytics
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_inactive_users(session: AsyncSession, inactive_period: timedelta) -> List[User]:
        cutoff_date = datetime.utcnow() - inactive_period
        query = select(User).where(User.last_login_at < cutoff_date)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_conversion_rate(session: AsyncSession, start_date: datetime, end_date: datetime) -> Dict:
        try:
            # Count total anonymous users
            anonymous_query = select(func.count(UserAnalytics.session_id.distinct()))\
                .where(UserAnalytics.event_type == "visit")\
                .where(UserAnalytics.previous_role == UserRole.ANONYMOUS)\
                .where(UserAnalytics.timestamp.between(start_date, end_date))
            
            # Count converted users
            converted_query = select(func.count(UserAnalytics.session_id.distinct()))\
                .where(UserAnalytics.event_type == "conversion")\
                .where(UserAnalytics.previous_role == UserRole.ANONYMOUS)\
                .where(UserAnalytics.new_role == UserRole.AUTHENTICATED)\
                .where(UserAnalytics.timestamp.between(start_date, end_date))

            # Execute both queries
            anonymous_result = await session.execute(anonymous_query)
            converted_result = await session.execute(converted_query)

            # Get the results
            total_anonymous = anonymous_result.scalar() or 0
            total_converted = converted_result.scalar() or 0

            # Calculate conversion rate
            conversion_rate = (total_converted / total_anonymous * 100) if total_anonymous > 0 else 0

            return {
                "total_anonymous": total_anonymous,
                "total_converted": total_converted,
                "conversion_rate": round(conversion_rate, 2)
            }
        except Exception as e:
            await session.rollback()
            raise e
  
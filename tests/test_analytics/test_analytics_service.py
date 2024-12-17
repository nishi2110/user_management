import pytest
from datetime import datetime, timedelta
from sqlalchemy import select
from app.services.analytics_service import AnalyticsService
from app.models.user_model import UserRole
from app.models.analytics_model import UserAnalytics
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_track_event(session):
    try:
        await AnalyticsService.track_event(
            session,
            "login",
            "test_session",
            None,
            UserRole.ANONYMOUS,
            UserRole.AUTHENTICATED
        )
        await session.commit()
        
        # Verify event was tracked
        result = await session.execute(select(UserAnalytics))
        analytics = result.scalars().first()
        assert analytics is not None
        assert analytics.event_type == "login"
    except Exception:
        await session.rollback()
        raise

@pytest.mark.asyncio
async def test_get_inactive_users(session, verified_user):
    # Set last login to 2 days ago
    verified_user.last_login_at = datetime.utcnow() - timedelta(days=2)
    await session.commit()

    inactive_users = await AnalyticsService.get_inactive_users(
        session,
        timedelta(days=1)
    )
    assert verified_user in inactive_users

@pytest.mark.asyncio
async def test_conversion_rate(session):
    try:
        # Create some test data with explicit timestamps
        start_date = datetime.utcnow()
        
        # First track the anonymous visit
        visit_event = await AnalyticsService.track_event(
            session,
            "visit",
            "session1",
            None,
            UserRole.ANONYMOUS,
            None
        )
        await session.commit()
        assert visit_event is not None
        assert visit_event.event_type == "visit"
        
        # Add a small delay
        await asyncio.sleep(0.1)
        
        # Then track the conversion of the same session
        conversion_event = await AnalyticsService.track_event(
            session,
            "conversion",
            "session1",
            None,
            UserRole.ANONYMOUS,
            UserRole.AUTHENTICATED
        )
        await session.commit()
        assert conversion_event is not None
        assert conversion_event.event_type == "conversion"
        
        # Add another small delay
        await asyncio.sleep(0.1)
        end_date = datetime.utcnow()

        # Get conversion stats
        stats = await AnalyticsService.get_conversion_rate(
            session,
            start_date,
            end_date
        )

        assert stats["total_anonymous"] == 1, "Should have one anonymous visit"
        assert stats["total_converted"] == 1, "Should have one conversion"
        assert stats["conversion_rate"] == 100.0, "Should have 100% conversion rate"
    except Exception:
        await session.rollback()
        raise
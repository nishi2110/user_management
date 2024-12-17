import pytest
from datetime import datetime, timedelta
from sqlalchemy import select
from app.services.analytics_service import AnalyticsService
from app.models.user_model import UserRole
from app.models.analytics_model import UserAnalytics
import asyncio

@pytest.mark.asyncio
async def test_track_event(db_session):
    await AnalyticsService.track_event(
        db_session,
        "login",
        "test_session",
        None,
        UserRole.ANONYMOUS,
        UserRole.AUTHENTICATED
    )
    # Verify event was tracked
    result = await db_session.execute(select(UserAnalytics))
    analytics = result.scalars().first()
    assert analytics is not None
    assert analytics.event_type == "login"

@pytest.mark.asyncio
async def test_get_inactive_users(db_session, verified_user):
    # Set last login to 2 days ago
    verified_user.last_login_at = datetime.utcnow() - timedelta(days=2)
    await db_session.commit()

    inactive_users = await AnalyticsService.get_inactive_users(
        db_session,
        timedelta(days=1)
    )
    assert verified_user in inactive_users

@pytest.mark.asyncio
async def test_conversion_rate(db_session):
    # Create some test data with explicit timestamps
    start_date = datetime.utcnow()
    
    # First track the anonymous visit
    visit_event = await AnalyticsService.track_event(
        db_session,
        "visit",
        "session1",
        None,
        UserRole.ANONYMOUS,
        None
    )
    assert visit_event is not None
    assert visit_event.event_type == "visit"
    
    # Add a small delay
    await asyncio.sleep(0.1)
    
    # Then track the conversion of the same session
    conversion_event = await AnalyticsService.track_event(
        db_session,
        "conversion",
        "session1",
        None,
        UserRole.ANONYMOUS,
        UserRole.AUTHENTICATED
    )
    assert conversion_event is not None
    assert conversion_event.event_type == "conversion"
    
    # Add another small delay
    await asyncio.sleep(0.1)
    end_date = datetime.utcnow()

    # Debug: Print the events and their timestamps
    result = await db_session.execute(
        select(UserAnalytics).where(UserAnalytics.session_id == "session1")
    )
    events = result.scalars().all()
    assert len(events) == 2, "Should have two events for the session"
    
    print("\nDebug - Events in database:")
    for event in events:
        print(f"Event type: {event.event_type}")
        print(f"Timestamp: {event.timestamp}")
        print(f"Previous role: {event.previous_role}")
        print(f"New role: {event.new_role}")
        print("---")

    # Get conversion stats
    stats = await AnalyticsService.get_conversion_rate(
        db_session,
        start_date,
        end_date
    )

    # Debug output
    print("\nDebug - Conversion stats:")
    print(f"Start date: {start_date}")
    print(f"End date: {end_date}")
    print(f"Total anonymous: {stats['total_anonymous']}")
    print(f"Total converted: {stats['total_converted']}")
    print(f"Conversion rate: {stats['conversion_rate']}")

    # Debug the queries
    anonymous_query = select(UserAnalytics)\
        .where(UserAnalytics.event_type == "visit")\
        .where(UserAnalytics.previous_role == UserRole.ANONYMOUS)\
        .where(UserAnalytics.timestamp.between(start_date, end_date))
    
    result = await db_session.execute(anonymous_query)
    anonymous_events = result.scalars().all()
    print("\nDebug - Anonymous visits found:")
    for event in anonymous_events:
        print(f"Event ID: {event.id}")
        print(f"Event type: {event.event_type}")
        print(f"Timestamp: {event.timestamp}")
        print("---")

    assert stats["total_anonymous"] == 1, "Should have one anonymous visit"
    assert stats["total_converted"] == 1, "Should have one conversion"
    assert stats["conversion_rate"] == 100.0, "Should have 100% conversion rate"
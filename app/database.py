from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
from settings.config import settings

# Create base class for declarative models
Base = declarative_base()

# Import all models to ensure they're registered with Base
from app.models.user_model import User  # noqa
from app.models.analytics_model import UserAnalytics  # noqa

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,
    poolclass=StaticPool if settings.database_url.startswith('sqlite') else None,
    isolation_level='SERIALIZABLE'
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=True
)

async def get_db() -> AsyncSession:
    """Dependency that provides a database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Export get_db
__all__ = ['Base', 'get_db', 'engine', 'AsyncSessionLocal']

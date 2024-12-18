from datetime import timedelta
from unittest.mock import AsyncMock
import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

from app.main import app
from app.database import Base, Database
from app.models.user_model import User, UserRole
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password
from app.services.jwt_service import create_access_token
from app.services.email_service import EmailService

# Global variables
fake = Faker()
settings = get_settings()

# Database configuration
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL, echo=settings.debug)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)

# Global fixtures
@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    """Initialize the database once per test session."""
    try:
        Database.initialize(settings.database_url)
    except Exception as e:
        pytest.fail(f"Failed to initialize the database: {str(e)}")


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Set up and tear down the database for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session():
    """Provide a database session for each test."""
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope="function")
async def async_client(db_session):
    """Provide an asynchronous HTTP client."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        app.dependency_overrides[get_db] = lambda: db_session
        try:
            yield client
        finally:
            app.dependency_overrides.clear()


# User fixtures
async def create_user(db_session, **kwargs):
    """Utility function to create a user with specified attributes."""
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
        **kwargs,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user


@pytest.fixture(scope="function")
async def locked_user(db_session):
    return await create_user(
        db_session,
        email_verified=False,
        is_locked=True,
        failed_login_attempts=settings.max_login_attempts,
    )


@pytest.fixture(scope="function")
async def user(db_session):
    return await create_user(db_session)


@pytest.fixture(scope="function")
async def verified_user(db_session):
    return await create_user(db_session, email_verified=True)


@pytest.fixture(scope="function")
async def unverified_user(db_session):
    return await create_user(db_session, email_verified=False)


@pytest.fixture(scope="function")
async def users_with_same_role_50_users(db_session):
    users = []
    for _ in range(50):
        user = await create_user(db_session)
        users.append(user)
    return users


@pytest.fixture(scope="function")
async def admin_user(db_session):
    return await create_user(
        db_session,
        nickname="admin_user",
        email="admin@example.com",
        role=UserRole.ADMIN,
    )


@pytest.fixture(scope="function")
async def manager_user(db_session):
    return await create_user(
        db_session,
        nickname="manager_user",
        email="manager_user@example.com",
        role=UserRole.MANAGER,
    )


# Token fixtures
@pytest.fixture(scope="function")
def admin_token(admin_user):
    token_data = {"sub": str(admin_user.id), "role": admin_user.role.name}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))


@pytest.fixture(scope="function")
def manager_token(manager_user):
    token_data = {"sub": str(manager_user.id), "role": manager_user.role.name}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))


@pytest.fixture(scope="function")
def user_token(user):
    token_data = {"sub": str(user.id), "role": user.role.name}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))


# Email service fixture
@pytest.fixture(scope="function")
def email_service():
    if settings.send_real_mail == "true":
        return EmailService()
    else:
        mock_service = AsyncMock(spec=EmailService)
        mock_service.send_verification_email.return_value = None
        mock_service.send_user_email.return_value = None
        return mock_service

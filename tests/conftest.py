"""
File: test_database_operations.py

Overview:
This Python test file utilizes pytest to manage database states and HTTP clients for testing a web application built with FastAPI and SQLAlchemy. It includes detailed fixtures to mock the testing environment, ensuring each test is run in isolation with a consistent setup.

Fixtures:
- `async_client`: Manages an asynchronous HTTP client for testing interactions with the FastAPI application.
- `db_session`: Handles database transactions to ensure a clean database state for each test.
- User fixtures (`user`, `locked_user`, `verified_user`, etc.): Set up various user states to test different behaviors under diverse conditions.
- `token`: Generates an authentication token for testing secured endpoints.
- `initialize_database`: Prepares the database at the session start.
- `setup_database`: Sets up and tears down the database before and after each test.
"""

# Standard library imports
from builtins import Exception, range, str
from datetime import timedelta
from unittest.mock import AsyncMock, patch
from uuid import uuid4
import asyncio

# Third-party imports
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from faker import Faker

# Application-specific imports
from app.main import app
from app.database import Base
from app.models.user_model import User, UserRole
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import create_access_token

fake = Faker()

settings = get_settings()

# Create test engine with specific SQLite settings
engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
    echo=False
)

# Create session factory
TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Create test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(autouse=True)
async def session():
    """Create a fresh database session for each test"""
    # Start outer transaction
    connection = await engine.connect()
    transaction = await connection.begin()

    # Create session
    session = TestingSessionLocal(bind=connection)
    await session.begin()

    # Override dependency
    app.dependency_overrides[get_db] = lambda: session

    try:
        # Clean tables
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

        yield session

    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()
        app.dependency_overrides.clear()

@pytest.fixture
async def client(session):
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.fixture(scope="function")
async def locked_user(session):
    unique_email = fake.email()
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": True,
        "failed_login_attempts": settings.max_login_attempts,
    }
    user = User(**user_data)
    session.add(user)
    await session.commit()
    return user

@pytest.fixture(scope="function")
async def user(session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
    }
    user = User(**user_data)
    session.add(user)
    await session.commit()
    return user

@pytest.fixture(scope="function")
async def verified_user(session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": True,
        "is_locked": False,
    }
    user = User(**user_data)
    session.add(user)
    await session.commit()
    return user

@pytest.fixture(scope="function")
async def unverified_user(session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
    }
    user = User(**user_data)
    session.add(user)
    await session.commit()
    return user

@pytest.fixture(scope="function")
async def users_with_same_role_50_users(session):
    users = []
    for _ in range(50):
        user_data = {
            "nickname": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "hashed_password": fake.password(),
            "role": UserRole.AUTHENTICATED,
            "email_verified": False,
            "is_locked": False,
        }
        user = User(**user_data)
        session.add(user)
        users.append(user)
    await session.commit()
    return users

@pytest.fixture
async def admin_user(session: AsyncSession):
    user = User(
        nickname=f"admin_{uuid4().hex[:8]}",
        email=f"admin_{uuid4().hex[:8]}@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="securepassword",
        role=UserRole.ADMIN,
        is_locked=False,
    )
    session.add(user)
    await session.commit()
    return user

@pytest.fixture
async def manager_user(session: AsyncSession):
    user = User(
        nickname=f"manager_{uuid4().hex[:8]}",
        email=f"manager_{uuid4().hex[:8]}@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="securepassword",
        role=UserRole.MANAGER,
        is_locked=False,
    )
    session.add(user)
    await session.commit()
    return user

# Configure a fixture for each type of user role you want to test
@pytest.fixture(scope="function")
def admin_token(admin_user):
    # Assuming admin_user has an 'id' and 'role' attribute
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

@pytest.fixture
def email_service():
    if settings.send_real_mail == 'true':
        # Return the real email service when specifically testing email functionality
        return EmailService()
    else:
        # Otherwise, use a mock to prevent actual email sending
        mock_service = AsyncMock(spec=EmailService)
        mock_service.send_verification_email.return_value = None
        mock_service.send_user_email.return_value = None
        return mock_service

@pytest.fixture(scope="function")
async def async_client(session):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        app.dependency_overrides[get_db] = lambda: session
        try:
            yield client
        finally:
            app.dependency_overrides.clear()

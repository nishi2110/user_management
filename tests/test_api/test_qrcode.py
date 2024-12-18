import pytest
from httpx import AsyncClient
from app.main import app
from app.database import Database, Base
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, UserRole, Invitation, InvitationStatus
from sqlalchemy.exc import IntegrityError


# Fixture for the test client
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


# Fixture for the test database session
@pytest.fixture(scope="module")
async def db_session():
    async with Database.get_session_factory()() as session:
        async with session.begin():
            # Create all tables
            await session.run_sync(Base.metadata.create_all)
        yield session
        async with session.begin():
            # Drop all tables
            await session.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_user_creation_endpoint(client: AsyncClient):
    """Test the User Creation Endpoint."""
    payload = {
        "nickname": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = await client.post("/users/", json=payload)
    assert response.status_code == 201, f"Unexpected response: {response.json()}"
    assert response.json()["nickname"] == "testuser"


@pytest.mark.asyncio
async def test_invitation_acceptance_workflow(client: AsyncClient, db_session: AsyncSession):
    """Test the Invitation Acceptance Workflow."""
    # Create a user to send the invitation
    inviter = User(
        nickname="inviter",
        email="inviter@example.com",
        hashed_password="hashed_password",
        role=UserRole.AUTHENTICATED
    )
    db_session.add(inviter)
    await db_session.commit()

    # Create an invitation
    invitation = Invitation(
        inviter_id=inviter.id,
        invitee_email="invitee@example.com",
        invitee_name="Invitee Name",
        qr_code_url="http://example.com/qrcode.png",
    )
    db_session.add(invitation)
    await db_session.commit()

    # Accept the invitation
    response = await client.post(f"/invitations/accept/{invitation.id}")
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert response.json()["status"] == "ACCEPTED"


@pytest.mark.asyncio
async def test_token_generation_and_validation(client: AsyncClient):
    """Test Token Generation and Validation."""
    payload = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = await client.post("/auth/token", json=payload)
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    token = response.json()["access_token"]
    assert token

    # Validate the token
    validation_response = await client.get("/auth/validate", headers={"Authorization": f"Bearer {token}"})
    assert validation_response.status_code == 200, f"Unexpected response: {validation_response.json()}"


@pytest.mark.asyncio
async def test_error_handling_for_invalid_inputs(client: AsyncClient):
    """Test Error Handling for Invalid Inputs."""
    payload = {
        "nickname": "short",
        "email": "invalid-email",
        "password": "123"
    }
    response = await client.post("/users/", json=payload)
    assert response.status_code == 422, f"Unexpected response: {response.json()}"


@pytest.mark.asyncio
async def test_database_rollback_on_failure(db_session: AsyncSession):
    """Test Database Rollback on Failure."""
    user = User(
        nickname="rollbackuser",
        email="rollbackuser@example.com",
        hashed_password="hashed_password",
        role=UserRole.AUTHENTICATED,
    )
    db_session.add(user)
    await db_session.commit()

    # Simulate a failure and rollback
    with pytest.raises(IntegrityError):
        db_session.add(User(
            nickname="rollbackuser",
            email="rollbackuser@example.com",
            hashed_password="hashed_password",
            role=UserRole.AUTHENTICATED
        ))
        await db_session.commit()

    # Ensure the first user still exists
    fetched_user = await db_session.scalar(db_session.query(User).filter_by(email="rollbackuser@example.com"))
    assert fetched_user is not None


@pytest.mark.asyncio
async def test_dockerized_app_health_check(client: AsyncClient):
    """Test Dockerized App Health Check Endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_qr_code_generation_endpoint(client: AsyncClient):
    """Test QR Code Generation Endpoint."""
    payload = {
        "nickname": "testuser",
        "email": "qrtest@example.com"
    }
    response = await client.post("/qrcodes/", json=payload)
    assert response.status_code == 201, f"Unexpected response: {response.json()}"
    assert "qr_code_url" in response.json()


@pytest.mark.asyncio
async def test_user_authentication_workflow(client: AsyncClient):
    """Test User Authentication Workflow."""
    payload = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = await client.post("/auth/token", json=payload)
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_admin_endpoint_access_control(client: AsyncClient):
    """Test Admin Endpoint Access Control."""
    # Non-admin user
    payload = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    token_response = await client.post("/auth/token", json=payload)
    token = token_response.json().get("access_token")

    response = await client.get("/admin/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403, f"Unexpected response: {response.json()}"

    # Admin user
    admin_payload = {
        "email": "admin@example.com",
        "password": "adminpassword"
    }
    admin_token_response = await client.post("/auth/token", json=admin_payload)
    admin_token = admin_token_response.json().get("access_token")

    admin_response = await client.get("/admin/", headers={"Authorization": f"Bearer {admin_token}"})
    assert admin_response.status_code == 200, f"Unexpected response: {admin_response.json()}"


@pytest.mark.asyncio
async def test_api_rate_limiting(client: AsyncClient):
    """Test API Rate Limiting."""
    for _ in range(10):  # Assuming the rate limit is 10 requests
        response = await client.get("/rate-limited-endpoint/")
        assert response.status_code == 200, f"Unexpected response: {response.json()}"

    # Exceed rate limit
    response = await client.get("/rate-limited-endpoint/")
    assert response.status_code == 429, f"Unexpected response: {response.json()}"

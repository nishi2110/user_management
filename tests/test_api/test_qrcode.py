import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models import User, Invitation
from app.utils.security import hash_password
import uuid

# Database Configuration
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Fixtures
@pytest.fixture(scope="module")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield SessionLocal
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session(test_db):
    async with test_db() as session:
        yield session

@pytest.fixture(scope="function")
async def async_client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def user(db_session):
    user = User(
        id=uuid.uuid4(),
        nickname="testuser",
        email="testuser@example.com",
        hashed_password=hash_password("securepassword"),
        role="AUTHENTICATED",
    )
    db_session.add(user)
    await db_session.commit()
    return user

# Test Cases
@pytest.mark.asyncio
async def test_create_invitation(async_client, user):
    response = await async_client.post(
        "/invite/",
        json={
            "inviter_id": str(user.id),
            "invitee_name": "John Doe",
            "invitee_email": "johndoe@example.com",
        },
    )
    assert response.status_code == 200
    assert "qr_code_url" in response.json()

@pytest.mark.asyncio
async def test_retrieve_sent_invitations(async_client, user, db_session):
    await async_client.post(
        "/invite/",
        json={
            "inviter_id": str(user.id),
            "invitee_name": "Jane Doe",
            "invitee_email": "janedoe@example.com",
        },
    )
    response = await async_client.get(f"/invites/?user_id={user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["sent"] == 1
    assert data["accepted"] == 0

@pytest.mark.asyncio
async def test_duplicate_invitation_email(async_client, user):
    invite_data = {
        "inviter_id": str(user.id),
        "invitee_name": "John Doe",
        "invitee_email": "johndoe@example.com",
    }
    await async_client.post("/invite/", json=invite_data)
    response = await async_client.post("/invite/", json=invite_data)
    assert response.status_code == 400
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_qr_code_generation(async_client, user):
    response = await async_client.post(
        "/invite/",
        json={
            "inviter_id": str(user.id),
            "invitee_name": "Jane Smith",
            "invitee_email": "janesmith@example.com",
        },
    )
    qr_code_url = response.json()["qr_code_url"]
    assert qr_code_url.endswith(".png")
    assert "qr_code_url" in response.json()

@pytest.mark.asyncio
async def test_accept_invitation(async_client, user, db_session):
    response = await async_client.post(
        "/invite/",
        json={
            "inviter_id": str(user.id),
            "invitee_name": "John Invitee",
            "invitee_email": "invitee@example.com",
        },
    )
    invite_id = response.json()["qr_code_url"].split("/")[-1].replace(".png", "")

    accept_response = await async_client.get(f"/accept/?invite={invite_id}")
    assert accept_response.status_code == 200
    assert "redirect_url" in accept_response.json()

@pytest.mark.asyncio
async def test_invalid_invitation_acceptance(async_client):
    response = await async_client.get("/accept/?invite=invalid-data")
    assert response.status_code == 400
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_revoke_invitation(async_client, user, db_session):
    response = await async_client.post(
        "/invite/",
        json={
            "inviter_id": str(user.id),
            "invitee_name": "Revoke Test",
            "invitee_email": "revoke@example.com",
        },
    )
    invite_id = response.json()["qr_code_url"].split("/")[-1].replace(".png", "")

    revoke_response = await async_client.patch(f"/admin/invites/{invite_id}/revoke")
    assert revoke_response.status_code == 200
    assert revoke_response.json()["status"] == "REVOKED"

@pytest.mark.asyncio
async def test_admin_list_invitations(async_client, user, db_session):
    for i in range(3):
        await async_client.post(
            "/invite/",
            json={
                "inviter_id": str(user.id),
                "invitee_name": f"User {i}",
                "invitee_email": f"user{i}@example.com",
            },
        )
    response = await async_client.get("/admin/invites/")
    assert response.status_code == 200
    assert len(response.json()) >= 3

@pytest.mark.asyncio
async def test_delete_invitation(async_client, user, db_session):
    response = await async_client.post(
        "/invite/",
        json={
            "inviter_id": str(user.id),
            "invitee_name": "Delete Test",
            "invitee_email": "delete@example.com",
        },
    )
    invite_id = response.json()["qr_code_url"].split("/")[-1].replace(".png", "")

    delete_response = await async_client.delete(f"/admin/invites/{invite_id}")
    assert delete_response.status_code == 200

@pytest.mark.asyncio
async def test_invalid_email_invitation(async_client, user):
    response = await async_client.post(
        "/invite/",
        json={
            "inviter_id": str(user.id),
            "invitee_name": "Invalid Email",
            "invitee_email": "invalid-email",
        },
    )
    assert response.status_code == 422

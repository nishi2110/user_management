from builtins import bool, int, str
from datetime import datetime
from enum import Enum
import uuid
from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean, func, ForeignKey, Enum as SQLAlchemyEnum, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


# User Roles Enum
class UserRole(str, Enum):
    """Enumeration of user roles within the application, stored as ENUM in the database."""
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


# Invitation Status Enum
class InvitationStatus(str, Enum):
    """Enumeration of invitation statuses."""
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REVOKED = "REVOKED"


# User Model
class User(Base):
    """
    Represents a user within the application, corresponding to the 'users' table in the database.
    """
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    bio: Mapped[str] = mapped_column(String(500), nullable=True)
    profile_picture_url: Mapped[str] = mapped_column(String(255), nullable=True)
    linkedin_profile_url: Mapped[str] = mapped_column(String(255), nullable=True)
    github_profile_url: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, name='UserRole', create_constraint=True), nullable=False, default=UserRole.AUTHENTICATED
    )
    is_professional: Mapped[bool] = mapped_column(Boolean, default=False)
    professional_status_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    verification_token: Mapped[str] = mapped_column(String, nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship with Invitation
    sent_invitations = relationship("Invitation", back_populates="inviter", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Provides a readable representation of a user object."""
        return f"<User {self.nickname}, Role: {self.role}>"

    def lock_account(self):
        """Locks the user account."""
        self.is_locked = True

    def unlock_account(self):
        """Unlocks the user account."""
        self.is_locked = False

    def verify_email(self):
        """Marks the user's email as verified."""
        self.email_verified = True

    def has_role(self, role_name: UserRole) -> bool:
        """Checks if the user has a specified role."""
        return self.role == role_name

    def update_professional_status(self, status: bool):
        """Updates the professional status and logs the update time."""
        self.is_professional = status
        self.professional_status_updated_at = func.now()


# Invitation Model
class Invitation(Base):
    """
    Represents an invitation sent by a user to invite another person to the application.
    """
    __tablename__ = "invitations"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inviter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    invitee_email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    invitee_name: Mapped[str] = mapped_column(String(100), nullable=False)
    qr_code_url: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[InvitationStatus] = mapped_column(
        SQLAlchemyEnum(InvitationStatus, name="InvitationStatus", create_constraint=True),
        default=InvitationStatus.PENDING,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with the inviter (User)
    inviter = relationship("User", back_populates="sent_invitations")

    def __repr__(self) -> str:
        """Provides a readable representation of an invitation."""
        return f"<Invitation {self.invitee_email}, Status: {self.status}>"

    def mark_accepted(self):
        """Marks the invitation as accepted and logs the time."""
        self.status = InvitationStatus.ACCEPTED


# QR Code Model
class QRCode(Base):
    """
    Represents a QR code entry in the database.
    """
    __tablename__ = "qrcodes"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)  # Data to encode in the QR code
    qr_code_url: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        """Provides a readable representation of a QR code entry."""
        return f"<QRCode ID: {self.id}, URL: {self.qr_code_url}>"

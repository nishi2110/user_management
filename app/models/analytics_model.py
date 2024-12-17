from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user_model import UserRole

class UserAnalytics(Base):
    __tablename__ = "user_analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    session_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    previous_role = Column(SQLAlchemyEnum(UserRole), nullable=True)
    new_role = Column(SQLAlchemyEnum(UserRole), nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    event_metadata = Column(String, nullable=True)

    user = relationship("User", back_populates="analytics")
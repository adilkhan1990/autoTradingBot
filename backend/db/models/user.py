from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)  # Optional for OAuth users
    name = Column(String, nullable=True)  # Full name from OAuth providers
    hashed_password = Column(String, nullable=True)  # Optional for OAuth users
    provider = Column(String, default="email")  # email, google, facebook, etc.
    provider_id = Column(String, nullable=True)  # OAuth provider user ID
    avatar_url = Column(Text, nullable=True)  # Profile picture URL
    email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

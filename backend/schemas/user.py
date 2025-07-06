from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    provider: str = "email"
    provider_id: Optional[str] = None
    avatar_url: Optional[str] = None
    email_verified: bool = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserInDBBase(UserBase):
    id: int
    provider: str
    provider_id: Optional[str] = None
    avatar_url: Optional[str] = None
    email_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: Optional[str] = None


# OAuth-specific schemas
class OAuthUserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    provider: str
    provider_id: str
    avatar_url: Optional[str] = None
    email_verified: bool = True

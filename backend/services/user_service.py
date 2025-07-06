from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import datetime

from db.models.user import User
from schemas.user import UserCreate, OAuthUserCreate, UserUpdate
from auth.utils import get_password_hash, verify_password


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_provider(self, provider: str, provider_id: str) -> Optional[User]:
        """Get user by OAuth provider and provider ID"""
        return self.db.query(User).filter(
            User.provider == provider, 
            User.provider_id == provider_id
        ).first()

    def authenticate_user(self, identifier: str, password: str) -> Optional[User]:
        """Authenticate user with email/username and password"""
        # Try to find user by email or username
        user = self.db.query(User).filter(
            or_(User.email == identifier, User.username == identifier)
        ).first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()
        return user

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with email/password"""
        # Generate username if not provided
        if not user_data.username:
            base_username = user_data.email.split("@")[0]
            user_data.username = self._generate_unique_username(base_username)

        # Hash password if provided
        hashed_password = None
        if user_data.password:
            hashed_password = get_password_hash(user_data.password)

        user = User(
            email=user_data.email,
            username=user_data.username,
            name=user_data.name,
            hashed_password=hashed_password,
            provider=user_data.provider,
            provider_id=user_data.provider_id,
            avatar_url=user_data.avatar_url,
            email_verified=user_data.email_verified,
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_oauth_user(self, oauth_data: OAuthUserCreate) -> User:
        """Create a new user from OAuth provider"""
        # Generate username from email
        base_username = oauth_data.email.split("@")[0]
        username = self._generate_unique_username(base_username)

        user = User(
            email=oauth_data.email,
            username=username,
            name=oauth_data.name,
            provider=oauth_data.provider,
            provider_id=oauth_data.provider_id,
            avatar_url=oauth_data.avatar_url,
            email_verified=oauth_data.email_verified,
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = user_data.dict(exclude_unset=True)
        
        # Handle password update
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def link_oauth_account(self, user_id: int, provider: str, provider_id: str, 
                          name: str = None, avatar_url: str = None) -> Optional[User]:
        """Link OAuth account to existing user"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        # Update OAuth information
        user.provider = provider
        user.provider_id = provider_id
        if name:
            user.name = name
        if avatar_url:
            user.avatar_url = avatar_url
        
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def _generate_unique_username(self, base_username: str) -> str:
        """Generate a unique username"""
        username = base_username
        counter = 1
        
        while self.get_user_by_username(username):
            username = f"{base_username}{counter}"
            counter += 1
            
        return username

    def user_exists(self, email: str = None, username: str = None) -> bool:
        """Check if user exists by email or username"""
        query = self.db.query(User)
        
        if email:
            query = query.filter(User.email == email)
        elif username:
            query = query.filter(User.username == username)
        else:
            return False
            
        return query.first() is not None

from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.user import User, UserCreate, OAuthUserCreate
from auth.utils import (
    create_access_token, 
    create_refresh_token, 
    get_current_user_from_token,
    verify_token
)
from core.config import settings
from db.base import get_db
from services.user_service import UserService

router = APIRouter()


@router.post("/login")
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user_service = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/register", response_model=User)
async def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Create new user account
    """
    user_service = UserService(db)
    
    # Check if user already exists
    if user_service.user_exists(email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if user_in.username and user_service.user_exists(username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Ensure password is provided for email registration
    if user_in.provider == "email" and not user_in.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required for email registration"
        )
    
    user = user_service.create_user(user_in)
    return user


@router.post("/oauth/register", response_model=User)
async def oauth_register(
    oauth_data: OAuthUserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register or login user via OAuth provider
    """
    user_service = UserService(db)
    
    # Check if user exists by provider
    user = user_service.get_user_by_provider(oauth_data.provider, oauth_data.provider_id)
    
    if user:
        # User exists, update last login
        user.last_login = datetime.utcnow()
        db.commit()
        return user
    
    # Check if user exists by email
    user = user_service.get_user_by_email(oauth_data.email)
    
    if user:
        # Link OAuth account to existing user
        user = user_service.link_oauth_account(
            user.id, oauth_data.provider, oauth_data.provider_id,
            oauth_data.name, oauth_data.avatar_url
        )
        return user
    
    # Create new OAuth user
    user = user_service.create_oauth_user(oauth_data)
    return user


@router.get("/me", response_model=User)
async def get_current_user(
    user_id: int = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get current user information
    """
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token
    """
    payload = verify_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id_str = payload.get("sub")
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token"
        )
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

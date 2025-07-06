from sqlalchemy.orm import Session
from db.base import engine, Base
from db.models.user import User


async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

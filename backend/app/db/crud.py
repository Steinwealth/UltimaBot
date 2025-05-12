# backend/app/db/crud.py

from sqlalchemy.orm import Session
from typing import Optional
from app.db.models import User
from app.core import schemas, security

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_in: schemas.UserCreate, is_admin: bool = False) -> User:
    hashed_password = security.get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

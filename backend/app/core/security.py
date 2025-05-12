# backend/app/core/security.py

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.db.database import SessionLocal
from app.db.crud import get_user_by_username
from app.db.models import User as DBUser

# === JWT CONFIGURATION ===
SECRET_KEY = os.getenv("SECRET_KEY", "ultima-secret-key")  # Load from env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# === PASSWORD CONTEXT ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === TOKEN SCHEME ===
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")  # Ensure your route matches

# === TOKEN CREATION ===
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# === PASSWORD UTILS ===
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# === USER FETCH ===
def get_user(username: str) -> Optional[DBUser]:
    db = SessionLocal()
    try:
        return get_user_by_username(db, username)
    finally:
        db.close()

# === AUTH VALIDATOR ===
def get_current_user(token: str = Depends(oauth2_scheme)) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError as e:
        print(f"[Security] JWT decode error: {e}")
        raise credentials_exception

    user = get_user(username)
    if not user or not user.is_active:
        raise credentials_exception
    return user

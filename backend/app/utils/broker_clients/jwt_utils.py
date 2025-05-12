# backend/app/utils/broker_clients/jwt_utils.py

import os
import jwt
from datetime import datetime, timedelta
from typing import Optional

# === JWT Configuration ===
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ULTIMA_BOT_SUPER_SECRET")  # Use env var in production
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 1440  # 24 hours

def create_token(data: dict, expires_in_minutes: Optional[int] = None) -> str:
    """
    Create a JWT token with expiration.
    """
    expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes or JWT_EXPIRATION_MINUTES)
    payload = {**data, "exp": expire}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token: str) -> Optional[dict]:
    """
    Decode a JWT token and return the payload if valid, or None if expired/invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("[JWTUtils] Token expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"[JWTUtils] Invalid token: {e}")
        return None

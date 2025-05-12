# backend/app/core/schemas.py

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# ==== Token Schema ====
class Token(BaseModel):
    access_token: str
    token_type: str

# ==== Token Payload ====
class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

# ==== User Base ====
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

# ==== Create New User ====
class UserCreate(UserBase):
    password: str

# ==== Login Request ====
class UserLogin(BaseModel):
    username: str
    password: str

# ==== User Model (for responses) ====
class User(UserBase):
    id: int
    is_active: bool = True
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True) 

# ==== UserInDB (internal) ====
class UserInDB(User):
    hashed_password: str

# ==== Login Response ====
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

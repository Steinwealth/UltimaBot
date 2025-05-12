# backend/app/core/models.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    id: Optional[int] = Field(default=None, description="Unique user ID")
    username: str = Field(..., description="Username used for login")
    full_name: Optional[str] = Field(default=None, description="Full name of the user")
    email: Optional[EmailStr] = Field(default=None, description="User email address")
    is_active: bool = Field(default=True, description="Is the user active?")
    is_admin: bool = Field(default=False, description="Is the user an administrator?")

    class Config:
        from_attributes = True  

# backend/app/db/__init__.py
"""
Database package initializer for Ultima Bot.
Provides SQLAlchemy Base, session handling, and CRUD/model imports.
"""

from .database import Base, SessionLocal, get_db
from . import models  # SQLAlchemy models (e.g., User)
from . import crud    # Reusable DB access functions

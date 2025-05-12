# backend/app/db/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

# Load the database URL from environment variables or fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/ultima")

# Create SQLAlchemy engine with connection pooling
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Configure session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session for FastAPI routes
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

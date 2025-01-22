from contextlib import contextmanager, asynccontextmanager

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session, Session

DATABASE_URL = "sqlite:///test.db"
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Async SQLite URL

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
# Base class for models
Base = declarative_base()

# Dependency to get the database session
@contextmanager
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def get_async_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


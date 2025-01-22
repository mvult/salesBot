from contextlib import contextmanager, asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, scoped_session, Session, DeclarativeBase

DATABASE_URL = "sqlite:///test.db"
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Async SQLite URL

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
# Base class for models
# Base = declarative_base()
class Base(DeclarativeBase):
    pass

# Dependency to get the database session
def get_db() :
    db = Session()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_managed_db() :
    db = Session()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def get_async_db()-> AsyncGenerator[AsyncSession, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


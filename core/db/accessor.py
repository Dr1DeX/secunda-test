from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from core.config import config

engine = create_async_engine(
    url=config.db_url,
    pool_recycle=3600,
    pool_size=config.DATABASE_POOL_SIZE,
    max_overflow=config.DATABASE_MAX_OVERFLOW,
    echo=config.DATABASE_ECHO,
    future=True,
    pool_pre_ping=True,
)

AsyncSessionFactory = async_sessionmaker(engine, autocommit=False, expire_on_commit=False)

Base = declarative_base()


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session

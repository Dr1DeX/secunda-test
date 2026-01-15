from fastapi.params import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache.pool import get_redis_pool
from core.db.accessor import get_db_session
from repositories.cache import CacheRepository
from repositories.directory import DirectoryRepository


async def get_cache_repository(redis: Redis = Depends(get_redis_pool)) -> CacheRepository:
    return CacheRepository(_redis=redis)


async def get_directory_repository(db_session: AsyncSession = Depends(get_db_session)) -> DirectoryRepository:
    return DirectoryRepository(_session=db_session)

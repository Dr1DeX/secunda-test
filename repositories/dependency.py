from core.cache.pool import get_redis_pool as redis
from repositories.cache import CacheRepository


async def get_cache_repository() -> CacheRepository:
    return CacheRepository(redis=redis())

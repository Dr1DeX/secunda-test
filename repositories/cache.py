from dataclasses import dataclass

import redis.asyncio as aioredis


@dataclass
class CacheRepository:
    _redis: aioredis.Redis

    async def ping(self):
        await self._redis.ping()

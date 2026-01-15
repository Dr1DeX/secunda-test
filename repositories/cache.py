from dataclasses import dataclass

import redis.asyncio as aioredis


@dataclass
class CacheRepository:
    redis: aioredis.Redis

    async def ping(self):
        await self.redis.ping()

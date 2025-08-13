from functools import lru_cache
import logging
from typing import Any

from redis.asyncio import Redis

from core.settings import settings


class RedisStorage(Redis):
    def __init__(self):
        super().__init__(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db,
            username=settings.redis.username,
            password=settings.redis.password,
        )

    async def get_record(self, key: str) -> Any | None:
        data = await self.get(name=key)
        if not data:
            logging.warning("No data by key %s in redis.", key)
            return None
        return data

    async def get_all_records(self, key: str) -> list[Any] | None:
        data = await self.lrange(name=key, start=0, end=-1)  # type: ignore
        if data:
            return [record for record in data]

    async def put_record(
        self, key: str, record: Any, expires_in: int | None = None
    ) -> None:
        expires_in = expires_in or settings.redis.expire
        await self.set(name=key, value=record, ex=expires_in)

    async def push_records(self, key: str, records: list[Any]) -> None:
        await self.rpush(name=key, *records)  # type: ignore
        await self.expire(name=key, time=settings.redis.expire)

    async def record_exists(self, key: str) -> bool:
        result = await self.exists(key)
        return bool(result)


redis_storage: RedisStorage | None = None


@lru_cache
def get_redis() -> RedisStorage | None:
    return redis_storage

import aioredis

class RedisConnectionManager:
    __redis_connection: aioredis.Redis = None

    @classmethod
    async def get_or_create_connection(cls) -> aioredis.Redis:
        if cls.__redis_connection is None:
            cls.__redis_connection = await aioredis.from_url('redis://redis:6379')
        return cls.__redis_connection

    @classmethod
    async def close_connection(cls):
        if cls.__redis_connection:
            await cls.__redis_connection.close()

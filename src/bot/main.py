import asyncio

from message_handlers import dp, bot
from redis_client import RedisConnectionManager


async def main():
    await dp.start_polling(bot)
    await RedisConnectionManager.close_connection()


if __name__ == '__main__':
    asyncio.run(main())

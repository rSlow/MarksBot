import asyncio

from config.bot import dp, bot


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())

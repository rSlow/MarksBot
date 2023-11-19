from aiogram import Bot, Dispatcher

from .router import root_router
from .settings import ENV
from .startup_shutdown import on_startup, on_shutdown
from .storage import redis_storage

token: str = ENV.str("BOT_TOKEN")

bot = Bot(
    token=token,
    parse_mode="HTML"
)
dp = Dispatcher(
    storage=redis_storage
)
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

dp.include_routers(
    root_router,
)

import logging

from aiogram import Bot, Dispatcher
from .middlewares import DbSessionMiddleware, ContextMiddleware
from .logger import init_logging
from .scheduler import scheduler, init_schedules
from .ui_config import set_ui_commands

from ORM.base import Session, stop_database


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    init_logging()

    dispatcher.update.middleware(ContextMiddleware(
        scheduler=scheduler,
    ))
    dispatcher.update.middleware(DbSessionMiddleware(session_pool=Session))

    await set_ui_commands(bot)

    scheduler.start()
    init_schedules(bot)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.info("SHUTDOWN")
    await bot.session.close()
    await stop_database()

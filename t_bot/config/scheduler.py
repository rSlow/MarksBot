from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings

scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)


def init_schedules(bot: Bot):
    # scheduler.add_job(
    #     func=send_birthdays,
    #     trigger="cron",
    #     hour=10,
    #     minute=00,
    #     kwargs={
    #         "bot": bot
    #     }
    # )
    ...

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings
from schedules import update_marks

scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)


def init_schedules(bot: Bot):
    scheduler.add_job(
        func=update_marks,
        trigger="interval",
        minutes=1,
        kwargs={
            "bot": bot,
            "mail": True
        }
    )

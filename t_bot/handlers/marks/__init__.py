from aiogram import Router

from handlers.marks.common import common_marks_router

marks_router = Router(name="marks")

marks_router.include_routers(
    common_marks_router,
)

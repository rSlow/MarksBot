from aiogram import Router

from handlers.main import first_router, last_router
from handlers.marks import marks_router
from handlers.admin import admin_router

root_router = Router(name="root")

root_router.include_routers(
    first_router,
    marks_router,
    admin_router,
    last_router
)

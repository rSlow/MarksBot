from handlers.admin.start import start_admin_router
from handlers.admin.update_marks import update_marks_router

from aiogram import Router

admin_router = Router(name="admin")

admin_router.include_routers(
    start_admin_router,
    update_marks_router
)

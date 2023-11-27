from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from FSM.admin import AdminState
from handlers.admin.start import start_admin
from keyboards.admin import StartAdminKeyboard
from schedules import update_marks as update_marks_func

update_marks_router = Router(name="admin_update_marks")


@update_marks_router.message(
    AdminState.start,
    F.text == StartAdminKeyboard.Buttons.update_marks
)
async def update_marks(message: types.Message, state: FSMContext, bot: Bot):
    service_message = await message.answer(
        text="Обновляю оценки..."
    )
    try:
        await update_marks_func(
            bot=bot,
            mail=False
        )
        await start_admin(
            message=message,
            state=state,
            text="Оценки обновлены."
        )
    finally:
        await service_message.delete()

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from FSM.admin import AdminState
from handlers.admin.start import start_admin
from keyboards.start import StartKeyboard
from schedules.update_marks import update_marks as update_marks_func

update_marks_router = Router(name="admin_update_marks")


@update_marks_router.message(
    AdminState.start,
    F.text == StartKeyboard.Buttons.admin
)
async def update_marks(message: types.Message, state: FSMContext):
    service_message = await message.answer(
        text="Обновляю оценки..."
    )
    try:
        await update_marks_func()
        await start_admin(
            message=message,
            state=state,
            text="Оценки обновлены."
        )
    finally:
        await service_message.delete()

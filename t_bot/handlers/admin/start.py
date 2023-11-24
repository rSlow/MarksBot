from FSM.admin import AdminState

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from FSM.start import CommonState
from filters import AdminFilter
from keyboards.admin import StartAdminKeyboard
from keyboards.start import StartKeyboard

start_admin_router = Router(name="start_admin")


@start_admin_router.message(
    AdminFilter(),
    CommonState.start,
    F.text == StartKeyboard.Buttons.admin
)
async def start_admin(message: types.Message, state: FSMContext, text: str | None = None):
    await state.set_state(AdminState.start)
    await message.answer(
        text=text or "Выберите действие:",
        reply_markup=StartAdminKeyboard.build()
    )

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from FSM.start import CommonState
from config.logger import logger
from keyboards.base.builder import BaseReplyKeyboardBuilder
from keyboards.start import StartKeyboard

first_router = Router(name="first")
last_router = Router(name="last")


@first_router.message(Command("start", "cancel"))
@first_router.message(F.text == BaseReplyKeyboardBuilder.on_main_button_text)
async def start(message: types.Message, state: FSMContext, text: str | None = None):
    await state.set_state(CommonState.start)
    await message.answer(
        text=text or "Какую информацию хотите получить?",
        reply_markup=StartKeyboard.build(
            validator_args={"user_id": message.chat.id}
        )
    )


@first_router.error()
async def error_pass(event: types.ErrorEvent, state: FSMContext):
    data = await state.get_data()
    message = event.update.message if event.update.message is not None else event.update.callback_query.message
    if isinstance(event.exception, KeyError) and not data:  # check if empty FSM data and KeyError exception
        await start(
            message=message,
            state=state,
            text=f"Бот был перезагружен, и промежуточные данные были утеряны. "
                 f"Попробуйте воспользоваться функцией еще раз."
        )
    else:
        await start(
            message=message,
            state=state,
            text=f"Извините, во время работы бота произошла ошибка. Мы вынуждены вернуть вас на главный экран. "
                 f"Попробуйте воспользоваться функцией еще раз."
        )
    logger.exception(event.exception)


@last_router.message(F.text)
async def delete(message: types.Message):
    await message.delete()

from keyboards.base.builder import BaseReplyKeyboardBuilder


class StartAdminKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        update_marks = "Обновить оценки"

    buttons_list = [
        Buttons.update_marks,
    ]

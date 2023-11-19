from config import settings
from .base.builder import BaseReplyKeyboardBuilder
from .base.validator import ButtonWithValidator, IsAdminValidator


class StartKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        two_faculty = "Двойки за факультет"
        two_today = "Двойки за сегодня"
        two_long_two_weeks = "Двойки более 2-х недель"
        two_top = "Топ двоечников"
        two_practice = "Двойки по практике"
        follow = "Подписка"
        admin = "Админка ⚙️"

    add_on_main_button = False

    def __init__(self):
        super().__init__()

        courses = settings.COURSES
        self.buttons_list = [
            [self.Buttons.two_faculty, self.Buttons.two_today],
            [self.Buttons.two_long_two_weeks, self.Buttons.two_top],
            [self.Buttons.two_practice, self.Buttons.follow],
            [f"{course} курс" for course in courses],
            [ButtonWithValidator(
                text=self.Buttons.admin,
                validator=IsAdminValidator()
            )],
        ]
        self.row_width = None

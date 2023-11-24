from abc import abstractmethod, ABC, abstractproperty
from enum import Enum, EnumType
from typing import Any, Optional, Type

from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder, ButtonType

from .validator import ButtonWithValidator


class TypeInterface(ABC):
    button_type = Any
    iterable = list[button_type] | tuple[button_type]
    double_iterable = list[iterable] | tuple[iterable]
    buttons_list_type = iterable | double_iterable


class ReplyTypeInterface(TypeInterface):
    button_type = str | KeyboardButton | EnumType | ButtonWithValidator


class InlineTypeInterface(TypeInterface):
    button_type = InlineKeyboardButton


class BaseKeyboardBuilder(KeyboardBuilder):
    buttons_list: Any = abstractproperty
    button_type: Type[ButtonType] = abstractproperty

    resize_keyboard: bool = True
    input_field_placeholder: str | None = None
    one_time_keyboard: bool | None = None
    is_persistent: bool | None = None
    selective: bool | None = None

    row_width: int | tuple[[int]] | None = 2

    add_on_main_button: bool = True
    on_main_button_text: str = "На главную ◀"

    validator_args: dict[str, Any] | None = None

    def __init__(self, **__):
        super().__init__(button_type=self.button_type)

    def _add_from_text(self, text: str):
        self.add(KeyboardButton(text=text))

    def as_markup(self):
        if self.buttons_list is None and not self.add_on_main_button:
            raise RuntimeError("buttons_list is not specified")
        else:
            self._process_buttons_list(self.buttons_list)

        if self.add_on_main_button:
            self._add_from_text(self.on_main_button_text)

        if self.row_width is not None:
            row_width = self.row_width
            if isinstance(row_width, int):
                row_width = (row_width,)
            self.adjust(*row_width)

        return super().as_markup(
            resize_keyboard=self.resize_keyboard,
            input_field_placeholder=self.input_field_placeholder,
            one_time_keyboard=self.one_time_keyboard,
            is_persistent=self.is_persistent,
            selective=self.selective
        )

    @classmethod
    def build(cls,
              validator_args: Optional[dict[str, Any]] = None,
              markup_args: Optional[dict[str, Any]] = None,
              **kwargs):
        keyboard = cls(**kwargs)
        if markup_args:
            for attr, value in markup_args.items():
                setattr(keyboard, attr, value)
        if validator_args:
            keyboard.validator_args = validator_args
        return keyboard.as_markup()

    @abstractmethod
    def _prepare_button(self, button: Any):
        pass

    def _process_buttons_list(self, buttons_list: TypeInterface.buttons_list_type):

        def _prepare_row(buttons_row: TypeInterface.iterable):
            prepared_row: list[KeyboardButton] = []
            for button in buttons_row:
                prepared_button = self._prepare_button(button)
                if prepared_button is not None:
                    prepared_row.append(prepared_button)
            return prepared_row

        for row in buttons_list:
            if isinstance(row, (list, tuple)):
                self.row(*_prepare_row(row))
            elif isinstance(row, (str, KeyboardButton, Enum, ButtonWithValidator, InlineKeyboardButton)):
                self.add(*_prepare_row(buttons_list))
                return


class BaseReplyKeyboardBuilder(BaseKeyboardBuilder):
    buttons_list: ReplyTypeInterface.button_type = []
    button_type: Type[ButtonType] = KeyboardButton

    def _prepare_button(self, button: ReplyTypeInterface.button_type):
        if isinstance(button, str):
            return self.button_type(text=button)

        elif isinstance(button, Enum):
            return self.button_type(text=button.value)

        elif isinstance(button, ButtonWithValidator):
            validator = button.validator
            matching_value = self.validator_args[validator.arg_name]
            if validator.validate(matching_value):
                return self.button_type(text=button.text)

        elif isinstance(button, KeyboardButton):
            return button

        else:
            raise TypeError(f"button {button} is not matches to "
                            f"'str', 'EnumType', 'KeyboardButton', 'ButtonWithValidator'")


class BaseInlineKeyboardBuilder(BaseKeyboardBuilder):
    add_on_main_button = False
    buttons_list: InlineTypeInterface.button_type = []
    button_type: Type[ButtonType] = InlineKeyboardButton

    def _prepare_button(self, button: InlineTypeInterface.button_type):
        if isinstance(button, InlineKeyboardButton):
            return button
        else:
            raise TypeError(f"button {button} is not matches to InlineKeyboardButton")


class CancelKeyboard(BaseReplyKeyboardBuilder):
    pass


class YesNoKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        yes = "Да"
        no = "Нет"

    buttons_list = [
        Buttons.yes,
        Buttons.no,
    ]

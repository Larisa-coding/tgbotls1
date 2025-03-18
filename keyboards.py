from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Задание 1: Основное меню
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

# Задание 2: URL-кнопки
links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Новости", url="https://news.google.com/"),
            InlineKeyboardButton(text="Музыка", url="https://music.youtube.com/"),
            InlineKeyboardButton(text="Видео", url="https://www.youtube.com/")
        ]
    ]
)

# Задание 3: Динамическая клавиатура
def dynamic_keyboard(show_more: bool = False):
    builder = InlineKeyboardBuilder()
    if not show_more:
        builder.add(InlineKeyboardButton(
            text="Показать больше",
            callback_data="show_more"
        ))
    else:
        builder.add(
            InlineKeyboardButton(text="Опция 1", callback_data="option_1"),
            InlineKeyboardButton(text="Опция 2", callback_data="option_2")
        )
    return builder.as_markup()
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")]],
                               resize_keyboard=True)

mood = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Позитивный"), KeyboardButton(text="Негативный")]],
                           resize_keyboard=True)
user_info = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Владелец бизнеса"), KeyboardButton(text="Сотрудник"), KeyboardButton(text="Фрилансер")]],
                           resize_keyboard=True)

order = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Высокий"), KeyboardButton(text="Любой")]],
                           resize_keyboard=True)
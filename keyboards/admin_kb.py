'''Кнопки клавиатуры Админа.'''

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btn_load = KeyboardButton('/Загрузить')
btn_delete = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(btn_load, btn_delete)

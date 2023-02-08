'''Клиентская клавиатура'''

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import time
import locale
#  удаление клавиатуры ReplyKeyboardRemove


locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

day_class = time.strftime('%A, %d %B')
# btn1 = KeyboardButton('Расписание')
btn2 = KeyboardButton('Адрес')
btn_today = KeyboardButton('Расписание на Сегодня')
btn_tmrrw = KeyboardButton('Завтра')
# btn4 = KeyboardButton('/Поделиться', request_contact=True)
btn5 = KeyboardButton('Где_я', request_location=True)

# клавиатура убирается с экрана , но не удаляется one_time_keyboard
# kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

# Варианты расположения кнопок меню
# kb_client.add(btn1).add(btn2).insert(btn3)
# kb_client.row(btn1, btn2, btn3).row(btn4, btn5)
# kb_client.add(btn1).row(btn2, btn3)
kb_client.row(btn_today, btn_tmrrw).row(btn2, btn5)

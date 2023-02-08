'''Клиентская часть БОТа.'''

from aiogram import Dispatcher, types
from create_bot import bot
from keyboards import kb_client
from . import sqlite_db


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               f'Привет, {message.from_user.first_name}!! Нажимай на кнопку РАСПИСАНИЕ,\
                                   чтобы узнать активности на сегодня и завтра.',
                               reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с БОТом через ЛС, напишите ему:'
                            '\nhttps://t.me/INZiRBot ')


# async def dialog_good(message: types.Message):
#     await message.reply('Отлично! Прерасный  настрой!')


# async def dialog_bad(message: types.Message):
#     await message.reply('Напиши куратору в личку, она обязательно поможет решить проблему!')


# @dp.message_handler(lambda message: 'такси' in message.text)
async def taxi(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'ТАКСИ:\n+79787000401\n+78692777777')


# @dp.message_handler(commands=['Режим_работы'])
# async def inzir_open_command(message: types.Message):
#     await bot.send_message(message.from_user.id,
#                            'ПН-ПТ с 8:30 до 17:30, СБ-ВС выходной'
#                            )


# @dp.message_handler(commands=['Адрес'])
async def inzir_location_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Обучение:\n    ул.Университетская, д.31, ауд.2.3'
                           '\nПроживание:\n ул.Лётчиков, д.5, "Омега-клуб"')

# Использовать, Если все написано в одном файле
# @dp.message_handler(commands=['Расписание'])
# async def inzir_calendar(message: types.Message):
#     for ret in cur.execute('SELECT * FROM menu').fetchall():
#         await bot.send_photo(
#             message.from_user.id,
#             ret[0],
#             f'{ret[1]}\nОписание: {ret[2]}\nНачало: {ret[-1]}')


# @dp.message_handler(commands=['Сегодня'])
async def inzir_calendar(message: types.Message):
    await sqlite_db.sql_read(message)


# @dp.message_handler(commands=['Завтра'])
async def inzir_tomorrow(message: types.Message):
    await sqlite_db.sql_read_tmrrow(message)


# @dp.message_handler(commands=['Завтра'])
async def inzir_all(message: types.Message):
    await sqlite_db.sql_read_all(message)


def registration_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(taxi,
                                lambda message: 'Такси' in message.text)
    # dp.register_message_handler(inzir_open_command, commands=['Режим_работы'])
    # dp.register_message_handler(dialog_bad,
    #                             lambda message: 'плохо' or 'помощь' in message.text)
    dp.register_message_handler(
        inzir_location_command,
        lambda message: 'Адрес' in message.text)
    dp.register_message_handler(
        inzir_calendar,
        lambda message: 'Сегодня' in message.text)
    dp.register_message_handler(
        inzir_tomorrow,
        lambda message: 'Завтра' in message.text)
    dp.register_message_handler(
        inzir_all,
        lambda message: 'расписание' in message.text)
    # dp.register_message_handler(dialog_good,
    #                             lambda message: 'хорошо' or 'отлично' in message.text)


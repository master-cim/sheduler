import string
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os, json, string

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот вышел в он-лайн')


'''Клиентская 0часть БОТа.'''
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет участник Летней школы ИНЖиР 2022!')
        await message.delete()
    except:
        await message.reply('Общение с БОТом через ЛС, напишите ему:'
                            '\nhttps://t.me/INZiRBot ')


@dp.message_handler(commands=['Режим_работы'])
async def inzir_open_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'ПН-ПТ с 8:30 до 17:30, СБ-ВС выходной')


@dp.message_handler(commands=['Адрес'])
async def inzir_location_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Обучение: ул.Университетская, д.31, ауд.2.3'
                           '\nПроживание: ул.Лётчиков, д.5, "Омега-клуб"')


# @dp.message_handler(commands=['Расписание'])
# async def inzir_calendar(message: types.Message):
#     for ret in cur.execute('SELECT * FROM menu').fetchall():
#         await bot.send_photo(
#             message.from_user.id,
#             ret[0],
#             f'{ret[1]}\nОписание: {ret[2]}\nНачало: {ret[-1]}')


'''Админская часть БОТа.'''



'''Общая часть БОТа.'''


@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(
        str.maketrans('', '', string.punctuation))
        for i in message.text.split(' ')}.intersection(
            set(json.load(open('cenz.json')))) != set():
            await message.reply('Грубость в чате запрещена')
            await message.delete()
    # if message.text == "Привет":
    #     await message.answer('Привет участник Летней школы ИНЖиР 2022!')
    # await message.reply(message.text)
    # await bot.send_message(message.from_user.id, message.text)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

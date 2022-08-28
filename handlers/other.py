from aiogram import types, Dispatcher
from create_bot import dp
import json
import string


'''Общая часть БОТа.'''
# @dp.message_handler()
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


def registration_handler_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)

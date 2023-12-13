'''Клиентская часть БОТа для второго курс.'''

import config
import os
import psycopg2 as ps
from os import listdir

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from aiogram.types import Message, CallbackQuery
import datetime


start_kb2 = ReplyKeyboardMarkup(resize_keyboard=True,)
start_kb2.row('Календарь')


@dp.message_handler(Text(equals=['Календарь'], ignore_case=True))
async def first_cal_handler(message: Message):
    await message.answer("Выбери дату: ",
                         reply_markup=await SimpleCalendar().start_calendar())


# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_first_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d-%m-%Y")}',
            reply_markup=start_kb2)
        day_start = date.strftime("%Y-%m-%d")
        sql_name = 'SELECT * FROM action WHERE class=1 AND day_start=%s ORDER BY time_start'
        cur.execute(sql_name, (day_start,))
        list_names = cur.fetchall()
        await callback_query.message.answer("<b>РАСПИСАНИЕ:</b>",
                            parse_mode="HTML")
        for ret in list_names:
            await callback_query.message.answer(
                    f'<b>{ret[1]}</b>\n{ret[2]}\n<i>Начало в:</i> {ret[3]}')
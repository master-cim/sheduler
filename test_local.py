'''Бот для информирования о расписании на сегодня и завтра.'''
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
import datetime
import random
import re
import nltk
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.neural_network import MLPClassifier

import json
import string
import time
# import locale


# locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
BOT_MESSAGE_TO_CHAT = '<b>Привет, участники группы!! я КИТ - твой помощник!</b>\
    <i>Я знаю единицы измерения электрических величин, владею информацией о стипендии.\
    Могу поддержать несложную беседу.</i>\
    <b>Очень жду!! Пиши в ЛС!!\nhttps://t.me/INZiRBot</b>'
ID = None
# DATABASE_URL = os.environ.get("DATABASE_URL")
# base = ps.connect(DATABASE_URL, sslmode='require')
# cur = base.cursor()
# cur_del = base.cursor()
storage = MemoryStorage()
# bot = Bot(token=os.environ.get("TOKEN"), parse_mode="HTML")
bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
TODAY = datetime.date.today()

# Шаг 1: собираем данные, на которых будет учиться модель
# data = json.load(open('intents_dataset.json'))
filename = "intents_dataset.json"

# Считываем файл в словарь
# with open(filename, 'r', encoding='UTF-8') as file:
INTENTS = json.load(open('intents_dataset.json', encoding="utf8"))

def clean_up(text):
    # преобразуем слово к нижнему регистру
    text = text.lower()
    # описываем текстовый шаблон для удаления: "все, что НЕ (^) является буквой \w или пробелом \s"
    re_not_word = r'[^\w\s]'
    # заменяем в исходном тексте то, что соответствует шаблону, на пустой текст (удаляем)
    text = re.sub(re_not_word, '', text)
    # возвращаем очищенный текст
    return text


def text_match(user_text, example):
    # допишем функцию так, чтобы все примеры ниже работали
    user_text = clean_up(user_text)
    example = clean_up(example)
    # A.find(B) - возвращает номер буквы, с которой идет текст B внутри текста А
    # find возвращает -1 в случае, если ничего не нашла
    # Устаревший вариант
    # if user_text.find(example) != -1:
    if example in user_text:
        return True
    # if example.find(user_text) != -1:
    #     return True
    example_len = len(example)
    difference = nltk.edit_distance(user_text, example)
    return (difference / example_len) < 0.35


# Определить намерение по тексту
def get_intent(user_text):
    for intent_name in INTENTS:
        # intent_name.lower()
        for example in INTENTS[intent_name]['examples']:
            if text_match(user_text, example):
                return intent_name
    return 'unknown'


# Берет случайный response для данного intent'а
def get_response(intent_name):
    # while intent_name != 'bye':
    return random.choice(INTENTS[intent_name]['responses'])


# async def on_startup(dp):
#     await bot.set_webhook(config.URL_APP)
#     print('Бот вышел в он-лайн')


# async def on_shutdown(dp):
#     await bot.delete_webhook()
#     cur.close()
#     cur_del.close()
#     base.close()
#     print('Бот вышел из он-лайн')

async def on_startup(_):
    print('Бот вышел в он-лайн')
    sql_start()


def sql_start():
    global base, cur, cur_del
    base = ps.connect(host="localhost", port=5432, database="postgres",
                      user="postgres", password="Ksu555aa")
    cur = base.cursor()
    cur_del = base.cursor()
    if base:
        print('Data base connected, OK!')


# Запрос нв добавление данных в PostgreSql
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO public.action(name, description, time_start, day_start, class)\
                VALUES (%s,%s,%s,%s,%s);', tuple(data.values()))
        base.commit()


# Запрос нв удаление данных из PostgreSql
async def sql_delete_command(data):
    with base:
        with base.cursor() as cur_del:
            cur_del.execute(
                'DELETE FROM public.action WHERE name_id = (%s);',
                (data, ))
    base.commit()


# Клиентская часть БОТа, активности на сегодня и завтра.
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id,
            f'Привет, {message.from_user.first_name}!!\
                Чтобы узнать активности на сегодня и завтра,\
             выбери, свой курс?',
            reply_markup=button_class)
        await message.delete()
    except:
        await message.reply('Общение с БОТом через ЛС, напишите ему:'
                            '\nhttps://t.me/INZiRBot ')


# Клиентская часть БОТа, активности на сегодня и завтра.
@dp.message_handler(lambda message: 'chatbot' in message.text)
async def bot_message_in_chat(message: types.Message):
    await message.answer(BOT_MESSAGE_TO_CHAT)
    await message.delete()


# Запрос клавиатуры расписания Первый курс
@dp.message_handler(lambda message: 'Первый курс' in message.text)
async def shedule_one(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери день',
                           reply_markup=kb_client1)


# Запрос клавиатуры расписания Второй курс
@dp.message_handler(lambda message: 'Второй курс' in message.text)
async def shedule_second(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери день',
                           reply_markup=kb_client2)


# Запрос расписания Первый курс на сегодня
@dp.message_handler(lambda message: '_Сегодня' in message.text)
async def edu_calendar(message: types.Message):
    await message.delete()
    day_class = time.strftime('%d.%m')
    await bot.send_message(message.from_user.id,
                           f'<b>Сегодня {day_class}:</b>')
    sql_name = 'SELECT * FROM action_today ORDER BY time_start'
    cur.execute(sql_name)
    list_names = cur.fetchall()
    await bot.send_message(message.from_user.id, "<b>РАСПИСАНИЕ:</b>",
                           parse_mode="HTML")
    for ret in list_names:
        await bot.send_message(
                message.from_user.id,
                f'<b>{ret[1]}</b>\n{ret[2]}\n<i>Начало в:</i> {ret[3]}')


# Запрос расписания Первый курс на завтра
@dp.message_handler(lambda message: 'Zавтра' in message.text)
async def edu_calendar_tomrr(message: types.Message):
    await message.delete()
    tomorrow = TODAY + datetime.timedelta(days=1)
    tmrr = tomorrow.strftime('%d.%m')
    await bot.send_message(message.from_user.id,
                           f'<b>Завтра {tmrr}:</b>')
    sql_name = 'SELECT * FROM public.action_tmrrw ORDER BY time_start'
    cur.execute(sql_name)
    list_names = cur.fetchall()
    for ret in list_names:
        await bot.send_message(
                message.from_user.id,
                f'<b>{ret[1]}</b>\n{ret[2]}\n<i>Начало в:</i> {ret[3]}')


# Запрос расписания Второй курс на сегодня
@dp.message_handler(lambda message: 'Сегодня_' in message.text)
async def edu_calendar2(message: types.Message):
    await message.delete()
    day_class = time.strftime('%d.%m')
    await bot.send_message(message.from_user.id,
                           f'<b>Сегодня {day_class}:</b>')
    sql_name = 'SELECT * FROM action_today_scond ORDER BY time_start'
    cur.execute(sql_name)
    list_names = cur.fetchall()
    await bot.send_message(message.from_user.id, "<b>РАСПИСАНИЕ</b>:")
    for ret in list_names:
        await bot.send_message(
                message.from_user.id,
                f'<b>{ret[1]}</b>\n{ret[2]}\n<i>Начало в:</i> {ret[3]}')


# Запрос расписания Второй курс на завтра
@dp.message_handler(lambda message: 'Завтра_' in message.text)
async def edu_calendar_tomrr2(message: types.Message):
    await message.delete()
    tomorrow = TODAY + datetime.timedelta(days=1)
    tmrr = tomorrow.strftime('%d.%m')
    await bot.send_message(message.from_user.id,
                           f'<b>Завтра {tmrr}:</b>')
    sql_name = 'SELECT * FROM public.action_tmrrw_scond ORDER BY time_start'
    cur.execute(sql_name)
    list_names = cur.fetchall()
    for ret in list_names:
        await bot.send_message(
                message.from_user.id,
                f'<b>{ret[1]}</b>\n{ret[2]}\n<i>Начало в:</i> {ret[3]}')


@dp.message_handler(lambda message: 'фотобота' in message.text)
async def bot_photo(message: types.Message):
    directory = "photos"
    photos = list()
    formats = ['.jpg', '.jpeg', '.png']
    for i in formats:
        for j in filter(lambda x: x.endswith(i), listdir(directory)):
            photos.append(j)
        # Вывксти все фотографии
        # for i in photos:
        #     with open(f"{directory}/{i}", 'rb') as photo:
        #         await bot.send_photo(chat_id=message.chat.id, photo=photo)
    # Вывести рандомно одно фото
    botfoto = random.choice(photos)
    with open(f"{directory}/{botfoto}", 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo)


# Запрос на адрес обучения
@dp.message_handler(commands=['Адрес'])
async def inzir_location_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Обучение: ул.Университетская, д.31, ауд.2.3'
                           )


# Получаем ИД текущего модератора
@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_commands(message: types.Message):
    global ID
    ID = message.from_user.id
    print(ID)
    await bot.send_message(message.from_user.id, 'Что хозяин надо???',
                           reply_markup=button_case_admin)
    await message.delete()


# Обработка комманд админа Машина состояний
class FSMAdmin(StatesGroup):

    name = State()
    description = State()
    start_time = State()
    day_start = State()
    sclass = State()


# Начало диалога загрузи навого Мероприятия
@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name.set()
        await message.reply('Введи название дисциплины:')


# Выход из состояния слово ОТМЕНА
@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Сброс')


# Ловим первый ответ и пишем его в словарь
@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    """Process название дисциплины."""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи вид занятия и ФИО препода:')


# Ловим второй ответ
@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply(
            'Введи время начала занятия\n формат: ЧЧ:ММ')


# Ловим третий ответ по времени мероприятия
@dp.message_handler(state=FSMAdmin.start_time)
async def load_start_time(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['start_time'] = message.text
        await FSMAdmin.next()
        await message.reply(
            'Введи дату занятия\n формат: ГГГГ-ММ-ДД')


# Ловим ответ по дате мероприятия
@dp.message_handler(state=FSMAdmin.day_start)
async def load_day_start(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['day_start'] = message.text
        await FSMAdmin.next()
        await message.reply(
            'Введи номер курса: 1 или 2')


# Ловим последний ответ по курсу и использем данные
@dp.message_handler(lambda message: message.text.isdigit(),
                    state=FSMAdmin.sclass)
async def load_sclass(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['class'] = int(message.text)
        await FSMAdmin.next()
        await sql_add_command(state)
        await state.finish()


# Удаление мероприятия
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(
        text=f'{callback_query.data.replace("del ", "")} удалена.',
        show_alert=True)


# Обработчик запроса на удаление
@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        query_all = 'SELECT * FROM public.select_all_data'
        cur_del.execute(query_all)
        read = cur_del.fetchall()
        # read = await sql_read2()
        for ret in read:
            await bot.send_message(
                message.from_user.id,
                f'{ret[0]}\n{ret[1]}\n{ret[2]}\n{ret[3]}Курс:{ret[-1]}')
            await bot.send_message(
                message.from_user.id, text='^^^',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                    f'Удалить {ret[0]}', callback_data=f'del {ret[0]}')))


# Диалог ИИ
@dp.message_handler()
async def echo_send(message: types.Message):
    intent = get_intent(message.text)
    answer = get_response(intent)
    await bot.send_message(message.from_user.id, answer)


@dp.message_handler()
async def echo_send_mat(message: types.Message):
    if {i.lower().translate(
        str.maketrans('', '', string.punctuation))
        for i in message.text.split(' ')}.intersection(
            set(json.load(open('cenz.json')))) != set():
        await message.reply('Грубость в чате запрещена')
        await message.delete()


# Обработка отсутствующих комманд всегда последняя
@dp.message_handler()
async def empty(message: types.Message):
    await message.answer('Нет такой команды!')
    await message.delete()


btn_today1 = KeyboardButton('_Сегодня')
btn_tmrrw1 = KeyboardButton('Zавтра')

btn_today2 = KeyboardButton('Сегодня_')
btn_tmrrw2 = KeyboardButton('Завтра_')

kb_client1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client1.row(btn_today1, btn_tmrrw1)

kb_client2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client2.row(btn_today2, btn_tmrrw2)

btn_class_f = KeyboardButton('Первый курс')
btn_class_s = KeyboardButton('Второй курс')

button_class = ReplyKeyboardMarkup(resize_keyboard=True)
button_class.row(btn_class_f, btn_class_s)

btn_load = KeyboardButton('/Загрузить')
btn_delete = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(btn_load, btn_delete)

# executor.start_webhook(
#     dispatcher=dp,
#     webhook_path='',
#     on_startup=on_startup,
#     on_shutdown=on_shutdown,
#     skip_updates=True,
#     host="0.0.0.0",
#     port=int(os.environ.get("PORT", 5000))
# )
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
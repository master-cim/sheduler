'''Админская часть БОТа.'''

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ID = None


class FSMAdmin(StatesGroup):

    photo = State()
    name = State()
    description = State()
    day_start = State()
    start_time = State()


# Получаем ИД текущего модератора
# dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_commands(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин надо???',
                           reply_markup=admin_kb.button_case_admin)
    await message.delete()


# Начало диалога загрузи навого Мероприятия
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузить фото')


# Выход из состояния
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Сброс')


# Ловим первый ответ и пишем его в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи название мероприятия:')


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи ФИО ведущего и описание:')


# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply(
            'Введи дату занятия\n формат: ДД.ММ')


# Ловим четверый ответ
# @dp.message_handler(state=FSMAdmin.start_time)
async def load_day_start(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['day_start'] = message.text
        await FSMAdmin.next()
        await message.reply(
            'Введи время начала занятия\n формат: ЧЧ:ММ')


# Ловим последний ответ и использем данные
# @dp.message_handler(state=FSMAdmin.start_time)
async def load_start_time(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['start_time'] = message.text
        await FSMAdmin.next()
        # отправлка в бот данных, которые будем сохранять
        # async with state.proxy() as data:
        #     await message.reply(str(data))
        await sqlite_db.sql_add_command(state)
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(
        text=f'{callback_query.data.replace("del ", "")} удалена.',
        show_alert=True)


# Удаление мероприятия
# @dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(
                message.from_user.id,
                ret[0], f'{ret[1]}\n {ret[2]}{ret[3]}\nНачало: {ret[4]} в {ret[-1]}')
            await bot.send_message(
                message.from_user.id, text='^^^',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                    f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


# Регистрируем хендлеры
def registration_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler,
                                Text(equals='отмена',
                                     ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'],
                                state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_day_start, state=FSMAdmin.day_start)
    dp.register_message_handler(load_start_time, state=FSMAdmin.start_time)
    dp.register_message_handler(make_changes_commands, commands=['moderator'],
                                is_chat_admin=True)
    dp.register_message_handler(delete_item, commands='Удалить')

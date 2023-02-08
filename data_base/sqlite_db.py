import sqlite3 as sq
from create_bot import bot
import time
import datetime
import locale


locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

# day_class = time.strftime('%d.%m')
# today = datetime.date.today()
# tomorrow = today + datetime.timedelta(days=1)
# tmrr = tomorrow.strftime('%d.%m')

# TD = f'SELECT * FROM action WHERE day_start like "{day_class}" ORDER BY time_start'
# TM = f'SELECT * FROM action WHERE day_start like "{tmrr}" ORDER BY time_start'
AL = 'SELECT * FROM action ORDER BY day_start, time_start'


def sql_start():
    global base, cur
    base = sq.connect('inzir.db')
    cur = base.cursor()
    if base:
        print('Data base connected, OK!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS action\
            (img TEXT,\
             name_id INTEGER PRIMARY KEY AUTOINCREMENT,\
             name TEXT,\
             description TEXT, day_start TEXT, time_start TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO action(img, name, description, day_start, time_start) VALUES(?, ?, ?, ?, ?)',
                    tuple(data.values()))
        base.commit()


# Запрос расписания занятий на сегодня
async def sql_read(message):
    day_class = time.strftime('%d.%m')
    for ret in cur.execute(
        f'SELECT * FROM action WHERE day_start like "{day_class}" ORDER BY time_start').fetchall():
        await bot.send_message(message.from_user.id,
                               f'РАСПИСАНИЕ на {ret[4]}')
        await bot.send_photo(
            message.from_user.id, ret[0],
            f'{ret[2]}\n     {ret[3]}\n     Начало в {ret[-1]}')


# Запрос расписания занятий на завтра
async def sql_read_tmrrow(message):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tmrr = tomorrow.strftime('%d.%m')
    for ret in cur.execute(
        f'SELECT * FROM action WHERE day_start like "{tmrr}" ORDER BY time_start').fetchall():
        await bot.send_message(message.from_user.id,
                               f'РАСПИСАНИЕ на {ret[4]}')
        await bot.send_photo(
            message.from_user.id, ret[0],
            f'{ret[2]}\n     {ret[3]}\n     Начало в: {ret[-1]}')


# Запрос расписания занятий полностью без картинок
async def sql_read_all(message):
    for ret in cur.execute(AL).fetchall():
        await bot.send_message(
            message.from_user.id,
            f'{ret[2]}\n     Дата: {ret[4]}\n     Начало в: {ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM action').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM action WHERE name_id == ?', (data,))
    base.commit()

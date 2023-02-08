from aiogram.utils import executor
from create_bot import dp
from handlers import admin, client, other
from . import sqlite_db


async def on_startup(_):
    print('Бот вышел в он-лайн')
    sqlite_db.sql_start()

client.registration_handler_client(dp)
admin.registration_handler_admin(dp)
other.registration_handler_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

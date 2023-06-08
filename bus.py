'''Расписание автобусов.
в переменную сохраняется текущая дата и время (час)
далее идет условие, если сегодня выходно/будни и текущий час больше или меньше 16, то в переменную сохраняется содержимое соответствующего текстового файла
далее в ответе выводится содержимое нужного текстового файла
'''
import time  # модуль для запуска раз в 5 секунд
import datetime  # модуль для работы с датой
from telebot import types

# сохраняем время и день недели
now = datetime.datetime.today().now()  # сохраняем в переменную текущее время, дату и день недели
weekday = datetime.datetime.today().weekday()  # сохраняем в переменную текущий день недели, отсчет с 0
current_hour = int(now.strftime("%H"))  # сохраняем в переменную текущий час в числовом формате

# Загружаем расписание автобусов в зависимости от дня недели и текущего времени
# выхи - утро
if (weekday == 5 or weekday == 6) and current_hour <= 16:
    temp1 = open('data/bus/weekend_morning_to_home.txt', 'r', encoding='UTF-8')
    bus_to_home = temp1.read()  # расписание автобусов домой
    temp1.close()

    temp2 = open('data/bus/weekend_morning_to_job.txt', 'r', encoding='UTF-8')
    bus_to_job = temp2.read()  # расписание автобусов на джоб
    temp2.close()

# выхи - вечер
elif (weekday == 5 or weekday == 6) and current_hour > 16:
    temp5 = open('data/bus/weekend_evening_to_home.txt', 'r', encoding='UTF-8')
    bus_to_home = temp5.read()  # расписание автобусов домой
    temp5.close()

    temp6 = open('data/bus/weekend_evening_to_job.txt', 'r', encoding='UTF-8')
    bus_to_job = temp6.read()  # расписание автобусов на джоб
    temp6.close()

# будни - утро
elif (weekday != 5 and weekday != 6) and current_hour <= 16:
    temp3 = open('data/bus/workday_morning_to_home.txt', 'r', encoding='UTF-8')
    bus_to_home = temp3.read()  # расписание автобусов домой
    temp3.close()

    temp4 = open('data/bus/workday_morning_to_job.txt', 'r', encoding='UTF-8')
    bus_to_job = temp4.read()  # расписание автобусов на джоб
    temp4.close()

# будни - вечер
elif (weekday != 5 and weekday != 6) and current_hour > 16:
    temp7 = open('data/bus/workday_evening_to_home.txt', 'r', encoding='UTF-8')
    bus_to_home = temp7.read()  # расписание автобусов домой
    temp7.close()

    temp8 = open('data/bus/workday_evening_to_job.txt', 'r', encoding='UTF-8')
    bus_to_job = temp8.read()  # расписание автобусов на джоб
    temp8.close()

else:
    bus_to_home = 'заглушка'
    bus_to_job = 'заглушка'


bot = telebot.TeleBot('1706338684:AAGojuK3Xw50cqr1osXwC6uvTRql0gQ-5cw')  # Создаем бота

@bot.message_handler(commands=["start"])  # Команда start
def start(m, res=False):
    # Добавляем кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Автобусы на джоб")
    item2 = types.KeyboardButton("Автобусы домой")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id,
                     'Нажми нужную кнопку',
                     reply_markup=markup)

@bot.message_handler(content_types=["text"])  # Получение сообщений от юзера
def handle_text(message):
    global answer  # костыль - делаем переменную глобальной, а то периодчески вылетает с ошибкой
    if message.text.strip() == 'Автобусы на джоб':  # Если юзер нажал на кнопку, выдаем ему расписание
        answer = bus_to_job
    elif message.text.strip() == 'Автобусы домой':  # Если юзер нажал на кнопку, выдаем ему расписание
        answer = bus_to_home

    # обновляем текущее время
    now = datetime.datetime.today().now()  # сохраняем в переменную текущее время, дату и день недели
    weekday = datetime.datetime.today().weekday()  # сохраняем в переменную текущий день недели, отсчет с 0
    current_hour = int(now.strftime("%H"))# сохраняем в переменную текущий час в числовом формате
    current_hour = 'Текущий час + 3 для расчетов: ' + str(current_hour + 3) + '\n' # добавляем к текущему часу 3
    current_time = 'Текущее время сервера: ' + now.strftime("%H:%M:%S") + '\n'  # текущее время

    answer += '\n' + current_hour + current_time  # добавление в вывод текущего времени и версии бота
    bot.send_message(message.chat.id, answer)  # Отсылаем юзеру сообщение в его чат

bot.polling(none_stop=True, interval=0)  # Запускаем бота
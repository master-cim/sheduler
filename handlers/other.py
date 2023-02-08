'''Общая часть БОТа.  Алгоритм — поиск по базе известных вопросов и ответов.'''

from aiogram import types, Dispatcher
from create_bot import dp
import json
import string
import random
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier


# Шаг 1: собираем данные, на которых будет учиться модель
# data = json.load(open('intents_dataset.json'))
filename = "intents_dataset.json"

# Считываем файл в словарь
# with open(filename, 'r', encoding='UTF-8') as file:
data = json.load(open('intents_dataset.json', encoding="utf8"))

# Создаем массивы фраз и интентов для обучения
X = []
y = []

for name in data:
    for phrase in data[name]['examples']:
        X.append(phrase)
        y.append(name)
    for phrase in data[name]['responses']:
        X.append(phrase)
        y.append(name)

# Векторизуем наши фразы X
vectorizer = CountVectorizer()
vectorizer.fit(X)
X_vec = vectorizer.transform(X)

# Создаем и обучаем модель
model_mlp = MLPClassifier()
model_mlp.fit(X_vec, y)

MODEL = model_mlp


def get_intent(text):
    # сначала преобразуем текст в числа
    text_vec = vectorizer.transform([text])
    # берем элемент номер 0 - для того, чтобы избавиться от формата "список", который необходим для векторизации и машинного обучения
    return model_mlp.predict(text_vec)[0] 


def get_response(intent):
    return random.choice(data[intent]['responses'])


async def echo_send(message: types.Message):
    intent_name = get_intent(message.text)
    answer = get_response(intent_name)
    await message.reply(answer)


async def echo_send_mat(message: types.Message):
    if {i.lower().translate(
        str.maketrans('', '', string.punctuation))
        for i in message.text.split(' ')}.intersection(
            set(json.load(open('cenz.json')))) != set():
        await message.reply('Грубость в чате запрещена')
        await message.delete()


def registration_handler_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
    dp.register_message_handler(echo_send_mat)

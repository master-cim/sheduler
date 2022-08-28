![](https://img.shields.io/badge/Python-3.7.5-green) 
![](https://img.shields.io/badge/Telegram-xx-blue) 
![](https://img.shields.io/badge/Heroku-zz-red) 
![](https://img.shields.io/badge/PostgreSql-2.9.3-yellow) 


# SHEDULER
Telegram Бот-ассистент, который будет обращаться к  БД PostgreSQL и узнавать расписание для 1 и 2 курса  
_Версия для облачного сервиса Heroku и БД PostgreSQL_

## :pencil2: Инструкции по запуску

Клонировать репозиторий, создать и активировать виртуальное окружение:

```sh
git clone https://github.com/master-cim/sheduler.git
cd sheduler
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Бот в одном файле sheduler_bot.py
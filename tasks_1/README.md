# tasks_1

Привет:)
Это тестовое задание но решил что это хороший тон иметь документацию к любому проекту

Описание проекта:
Этот проект представляет собой веб-приложение, которое позволяет пользователям:
1) Вводить дату рождения через Telegram WebApp.
2) Отображать количество дней, часов и минут до следующего дня рождения.
3) Делиться ссылкой на свои данные с другими пользователями.

Проект состоит из:
1) Frontend: Vue.js приложение, размещенное на Render (Static Site).
2) Backend: FastAPI сервер, размещенный на Render (Web Service). Но который не работает вот причина (https://stackoverflow.com/questions/66465408/postgresql-oserror-multiple-exceptions-errno-111-connect-call-failed-127-0)
   можно было запустить на heroku, было лень не сделал
3) База данных: PostgreSQL для хранения данных пользователей.


# Установка и настройка
1. Клонирование репозитория
```sh
git clone https://github.com/Tsyretorov/tests_tasks/tree/master/tasks_1
cd tasks_1
```
2. Настройка бэкенда
```sh
cd tg_bot_backend
pip install -r requirements.txt 
```
# Настройка бд
Вам нужно указать свой posgrestsql данные в файле webapp в конце строки url_db (line 74)

# Запуск сервера
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

# Настройка фронтенда
1. Установка зависимостей
```sh
cd tg_bot_frontend
npm install
```
2. Настройка переменных окружения
в файле vite.config.ts на 13 строке поставьте свой url для работы с backend
(это нужно для обхождения curs)
такеж в package.json на 5 стркое укажите свой url хоть и можно без него -_-
на этом все доп информация будет в README.md в tg_bot_frontend
















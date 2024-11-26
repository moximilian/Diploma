# Активировать виртуальное пространство

`cd /src/backend`

## Windows:
- `py -m venv .venv`
- `.\venv\Scripts\activate`

## On macOS and Linux:

- `python3 -m venv .venv`
- `source venv/bin/activate`

# Установка зависимостей:

__Необходимая версия Python > 3.11__

`pipenv install --ignore-pipfile`

# Запуск приложения через Docker:

`docker-compose --env-file app/.env.development.local up`

Перезапуск:

`docker-compose up --build`

API будет доступна на http://0.0.0.0:8000

For Production:

`docker-compose --env-file app/.env.production up`
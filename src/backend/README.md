# 1. Активировать виртуальное пространство

`cd /src/backend`

## Windows:
- `py -m venv .venv`
- `.\venv\Scripts\activate`

## macOS \ Linux:

- `python3 -m venv .venv`
- `source .venv/bin/activate`

## Установка зависимостей для локальной сборки:

__Необходимая версия Python > 3.11__

`pipenv install --ignore-pipfile`

# 2. Запуск приложения в Docker

## Первый запуск:

`docker-compose --env-file app/.env.development.local up`

## Последующие запуски :

`docker-compose up --build`

## Production сборка:

`docker-compose --env-file app/.env.production up`
## API

API будет доступна на http://0.0.0.0:8000


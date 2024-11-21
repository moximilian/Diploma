Активировать виртуальное пространство

Windows:
- venv\Scripts\activate

On macOS and Linux:

- source venv/bin/activate

For Development:

`docker-compose --env-file app/.env.development.local up`
For reload `docker-compose up --build`

API будет доступна на http://0.0.0.0:8000

For Production:

`docker-compose --env-file app/.env.production up`
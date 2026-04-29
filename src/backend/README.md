# 1. To start up locally, checkout to backend directory

`cd /src/backend`
# 2. Activate virtual space
## Windows:
- `py -m venv .venv`
- `.\venv\Scripts\activate`

## macOS \ Linux:

- `python3 -m venv .venv`
- `source .venv/bin/activate`

# 3. Install all required dependencies:

__Python > 3.11__

`pipenv install --ignore-pipfile`

# 4. Run the app in Docker

## Initial startup:

`docker-compose --env-file app/.env.development.local up`

## Further startups or restarts:

`docker-compose up --build`

# To build for production:

`docker-compose --env-file app/.env.production up`


__API will be avaliable at http://0.0.0.0:8000__


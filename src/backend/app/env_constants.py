import os
from dotenv import load_dotenv

ENV_PATH = '.env.development.local'

if not os.path.exists(ENV_PATH):
    print(f'Cant find your env file {ENV_PATH}')
    exit()

load_dotenv(dotenv_path=ENV_PATH)

POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB=os.getenv('POSTGRES_DB')
BASE_URL=os.getenv('BASE_URL')


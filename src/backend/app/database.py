from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from env_constants import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

if None in [POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]:
    print('Some of the params are empty and cant provide access to DB')
    exit()

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{
    POSTGRES_PASSWORD}@db/{POSTGRES_DB}'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

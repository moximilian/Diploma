from fastapi import FastAPI
from .database import engine
from . import models
from .api.api import app_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(app_router)
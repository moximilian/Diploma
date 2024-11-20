from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from api.api import app_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(app_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins if needed
    allow_credentials=True,
    allow_methods=["POST, GET"],
    allow_headers=["*"],
)

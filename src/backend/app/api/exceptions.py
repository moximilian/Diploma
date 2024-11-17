"""
Logic to work with API
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from main import app

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={'detail': 'Can not find requested route.', 'body': exc.body},
    )
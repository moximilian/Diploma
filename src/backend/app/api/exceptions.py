"""
Logic to work with API
"""
from fastapi import HTTPException

class BaseException(HTTPException):
    def __init__(self, code, message):
        super().__init__(status_code=code, detail=message)

class ValidationEror(BaseException):
    def __init__(self, message: str, field: str = None):
        detailed_message = {
            'message': message,
            'code': 400,
            'field': field
        }
        super().__init__(code=400, message=detailed_message)
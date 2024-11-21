"""
Logic to work with API
"""
from fastapi import HTTPException
import typing as t


class BaseException(HTTPException):
    def __init__(self, code: int, message: str, field: t.Union[str, list] = None):
        detailed_message = {
            'message': message,
            'code': code,
            'field': field
        }
        super().__init__(status_code=code, detail=detailed_message)


class ValidationEror(BaseException):
    def __init__(self, message: str = 'Validation Error', field: t.Union[str, list] = None):
        super().__init__(code=400, message=message, field=field)


class AuthorisationError(BaseException):
    def __init__(self, message: str = 'Incorrect username or password', field: t.Union[str, list] = None):
        super().__init__(code=401, message=message, field=field)

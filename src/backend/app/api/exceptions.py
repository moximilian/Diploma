"""
Logic to work with API
"""
from fastapi import HTTPException


class BaseException(HTTPException):
    def __init__(self, code: int, message: str, field: str | list = None):
        detailed_message = {
            'message': message,
            'code': code,
            'field': field
        }
        super().__init__(status_code=code, detail=detailed_message)


class ValidationEror(BaseException):
    def __init__(self, message: str = 'Validation Error', field: str | list = None):
        super().__init__(code=400, message=message, field=field)


class AuthorisationError(BaseException):
    def __init__(self, message: str = 'Incorrect username or password', field: str | list = None):
        super().__init__(code=401, message=message, field=field)


class NotFoundError(BaseException):
    def __init__(self, message: str = 'Requested item is not found', field: str | list = None):
        super().__init__(code=404, message=message, field=field)


class InternalError(BaseException):
    def __init__(self, message: str = 'Internal Error', field: str | list = None):
        super().__init__(code=500, message=message, field=field)


class ForbiddenError(BaseException):
    def __init__(self, message: str = 'Requested item is forbidden to read', field: str | list = None):
        super().__init__(code=403, message=message, field=field)

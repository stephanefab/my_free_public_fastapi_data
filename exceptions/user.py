from .base import AppException

class UserNotFoundError(AppException):
    pass

class UserAlreadyExistsError(AppException):
    pass
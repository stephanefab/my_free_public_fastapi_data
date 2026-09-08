from .base import AppException

class UserNotFoundError(AppException):
    status_code = 404

class UserAlreadyExistsError(AppException):
    status_code = 409
from .base import AppException

class UserNotFoundError(AppException):
    status_code = 404
    
    def __init__(self, detail):
        super().__init__(detail, "USER_NOT_FOUND")
    
class UserAlreadyExistsError(AppException):
    status_code = 409
class AppException(Exception):
    status_code = 400

    def __init__(self, detail: str, code: str = "APP_ERROR"):
        self.detail = detail
        self.code = code
        super().__init__(detail)
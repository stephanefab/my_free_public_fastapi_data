class AppException(Exception):
    status_code = 400
    
    def __init__(self, detail):
        self.detail = detail
        super().__init__(detail)


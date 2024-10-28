from enum import Enum
from typing import Dict, Any

class ErrorCode(Enum):
    INVALID_INPUT_VALUE = ("C001", "Invalid Input Value", 400)
    INTERNAL_SERVER_ERROR = ("C004", "Server Error", 500)
    USER_NOT_FOUND = ("U001", "User Not Found", 404)
    MOVIE_NOT_FOUND = ("M001", "Movie Not Found", 404)
    FAVORITE_NOT_FOUND = ("F001", "Favorite Not Found", 404)
    DUPLICATE_FAVORITE = ("F002", "Duplicate Favorite", 400)

    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code

class BusinessException(Exception):
    def __init__(self, error_code: ErrorCode, detail: str = None):
        self.error_code = error_code
        self.detail = detail

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.error_code.code,
            "message": self.error_code.message,
            "detail": self.detail
        }
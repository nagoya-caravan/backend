from dataclasses import dataclass
from enum import Enum

from app import app


@dataclass
class ErrorId:
    message: str
    status_code: int


class ErrorIds(Enum):
    INTERNAL_ERROR = ErrorId("server internal error", 500)


class ResponseException(Exception):
    def __init__(self, error_id: ErrorIds, message: str | None = None):
        if message is None:
            message = error_id.value.message
        self.error_id = error_id
        self.message = message


@app.errorhandler(ResponseException)
def response_exception(e: ResponseException):
    return {
        "error_id": e.error_id.name,
        "message": e.message
    }


@app.errorhandler(Exception)
def exception(e: Exception):
    return {
        "error_id": ErrorIds.INTERNAL_ERROR,
        "message": e.__str__()
    }

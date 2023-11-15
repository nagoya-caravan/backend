import traceback
from dataclasses import dataclass
from enum import Enum

from app import app


@dataclass
class ErrorId:
    message: str
    status_code: int


class ErrorIds(Enum):
    INTERNAL_ERROR = ErrorId("server internal error", 500)
    CALENDER_NOT_FOUND = ErrorId("calender not found", 400)
    USER_NOT_FOUND = ErrorId("user not found", 400)
    EVENT_NOT_FOUND = ErrorId("event not found", 400)
    ICAL_URL_NOT_FOUND = ErrorId("ical url not found", 400)
    ICAL_URL_NOT_VALID = ErrorId("ical url not valid", 400)
    ICAL_TXT_NOT_VALID = ErrorId("ical text is not valid", 400)


class ErrorIdException(Exception):
    def __init__(self, error_id: ErrorIds, message: str | None = None):
        if message is None:
            message = error_id.value.message
        self.error_id: ErrorIds = error_id
        self.message = message


@app.errorhandler(ErrorIdException)
def response_exception(e: ErrorIdException):
    return {
        "error_id": e.error_id.name,
        "message": e.message
    }, e.error_id.value.status_code


@app.errorhandler(Exception)
def exception(e: Exception):
    app.logger.warning(traceback.format_exc())
    return {
        "error_id": ErrorIds.INTERNAL_ERROR.name,
        "message": e.__str__()
    }, ErrorIds.INTERNAL_ERROR.value.status_code

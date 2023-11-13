import datetime

from flask import request


class TzOffset:
    default_offset = 9

    def __init__(self, offset: int):
        self.offset = offset

    @staticmethod
    def offset_by_query():
        offset = request.args.get("tz_offset", TzOffset.default_offset, int)
        return TzOffset(offset)

    def timezone(self):
        return datetime.timezone(datetime.timedelta(hours=self.offset))

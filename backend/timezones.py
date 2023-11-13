import datetime

from flask import request

default_offset = 9


def timezone_by_query():
    timezone = request.args.get("tz_offset", default_offset)
    timezone = datetime.timezone(datetime.timedelta(hours=timezone))
    return timezone

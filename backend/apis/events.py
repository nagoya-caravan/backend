import datetime
from dataclasses import asdict

from flask import request

from app import app
from backend.json import EventEditJson
from backend.manager import EventManager
from backend.util import DatetimeRange
from backend.util import datetime_formatter


@app.route("/api/event/<int:event_id>", methods=["PUT"])
def put_event(event_id: int):
    EventManager.edit(event_id, EventEditJson(**request.json))
    return {}


def get_datetime_range():
    start = request.args.get("start", None)
    if start is None:
        start = datetime.datetime.now()
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        start = datetime_formatter.str_to_date(start)

    end = request.args.get("end", None)
    if end is None:
        end = datetime.datetime.now()
        end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
    else:
        end = datetime_formatter.str_to_date(end)
    return DatetimeRange(start, end)


@app.route("/api/calender/<int:calender_id>/event", methods=["GET"])
def get_events(calender_id: int):
    result = list()

    datetime_range = get_datetime_range()
    for event in EventManager.event_by_calender(
            calender_id, datetime_range
    ):
        result.append(asdict(event))
    return result


@app.route("/api/calender/<int:calender_id>/public-event", methods=["GET"])
def get_public_events(calender_id: int):
    result = list()

    datetime_range = get_datetime_range()
    for event in EventManager.public_event_by_calender(
            calender_id, datetime_range
    ):
        result.append(asdict(event))
    return result

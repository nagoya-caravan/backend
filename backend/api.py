import datetime
from dataclasses import asdict

from flask import request

from app import app
from backend.formatter import datetime_formatter
from backend.json import CalenderJson, EventEditJson
from backend.manager import CalenderManager, EventManager
from backend.util import DatetimeRange


@app.route("/api/calender", methods=["POST"])
def post_calender():
    calender = CalenderJson(**request.json)
    return asdict(
        CalenderManager.create(calender)
    )


@app.route("/api/calender/<int:calender_id>", methods=["PUT"])
def put_calender(calender_id: int):
    calender = CalenderJson(**request.json)
    calender.calender_id = calender_id
    CalenderManager.edit(calender)
    return {}


@app.route("/api/calender/<int:calender_id>", methods=["GET"])
def get_calender(calender_id: int):
    return asdict(
        CalenderManager.get(calender_id)
    )


@app.route("/api/calender", methods=["GET"])
def get_calenders():
    result = list()
    for calender in CalenderManager.get_list(
            request.args.get("page", 0, int),
            request.args.get("size", 10, int)
    ):
        result.append(asdict(calender))
    return result


@app.route("/api/calender/<int:calender_id>/refresh", methods=["GET"])
def refresh_calender(calender_id: int):
    EventManager.refresh(calender_id)
    return {}


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

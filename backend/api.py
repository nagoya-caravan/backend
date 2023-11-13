from dataclasses import asdict

from flask import request

from app import app
from backend.json import CalenderJson, EventEditJson
from backend.manager import CalenderManager, EventManager


@app.route("/api/calender", methods=["POST"])
def post_calender():
    calender = CalenderJson(**request.json)
    return asdict(
        CalenderManager.create(calender.calender_name, calender.ical_urls)
    )


@app.route("/api/calender/<int:calender_id>", methods=["PUT"])
def put_calender(calender_id: int):
    calender = CalenderJson(**request.json)
    CalenderManager.edit(calender_id, calender.calender_name, calender.ical_urls)
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

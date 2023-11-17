from dataclasses import asdict

from flask import request

from app import app
from backend.json import CalenderJson
from backend.manager import CalenderManager, EventManager


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


@app.route("/api/calender/<int:calender_id>", methods=["DELETE"])
def delete_calender(calender_id: int):
    CalenderManager.delete(calender_id)
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

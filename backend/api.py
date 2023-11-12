from flask import request

from app import app
from backend.json import CalenderJson
from backend.manager import CalenderManager


@app.route("/api/calender", methods=["POST"])
def post_calender():
    calender = CalenderJson(**request.json)
    return CalenderManager.create(calender.calender_name, calender.ical_urls)


@app.route("/api/calender/<int:calender_id>", methods=["PUT"])
def put_calender(calender_id: int):
    calender = CalenderJson(**request.json)
    CalenderManager.edit(calender_id, calender.calender_name, calender.ical_urls)
    return {}

#
# @app.route("/api/calender/<int:calender_id>", methods=["GET"])
# def get_calender(calender_id: int):
#     calendar = CalenderJson(**request.json)
#     CalenderRepository.

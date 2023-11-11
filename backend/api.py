from flask import request, jsonify

from app import app
from backend.calender import CalenderJson, CalenderManager


@app.route("/api/calender", methods=["POST"])
def post_calender():
    calender = CalenderJson(**request.json)
    return CalenderManager.create(calender.calender_name, calender.ical_urls)

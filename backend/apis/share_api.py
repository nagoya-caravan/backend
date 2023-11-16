from dataclasses import asdict

from flask import request

from app import app
from backend.json import ShareJson
from backend.manager import ShareManager


@app.route("/api/calender/<int:calender_id>/share", methods=["PUT"])
def put_shares(calender_id: int):
    share = ShareJson(**request.json)
    share.calender_id = calender_id
    ShareManager.save(share)
    return {}


@app.route("/api/calender/<int:calender_id>/share", methods=["GET"])
def get_shares(calender_id: int):
    return asdict(ShareManager.get(calender_id))

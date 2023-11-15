from dataclasses import asdict

from flask import request

from app import app
from backend.json import UserJson
from backend.manager import UserManager


@app.route("/api/user", methods=["POST"])
def post_user():
    user_json = UserJson(**request.json)
    return asdict(
        UserManager.create(user_json)
    )


@app.route("/api/user", methods=["GET"])
def get_user():
    return asdict(UserManager.get_user_ornone())

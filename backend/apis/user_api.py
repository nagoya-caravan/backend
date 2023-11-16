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


@app.route("/api/user", methods=["PUT"])
def put_user():
    user_json = UserJson(**request.json)
    UserManager.edit(user_json)
    return {}


@app.route("/api/user", methods=["GET"])
def get_user():
    return asdict(UserManager.user_by_header())


@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_other_user(user_id: int):
    return asdict(UserManager.user_by_id(user_id))

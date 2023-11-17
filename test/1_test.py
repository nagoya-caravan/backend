from dataclasses import asdict

from app import db, app
from backend.model import CalenderModel, UserModel
from test import post_test, user1, calender1, delete_test


def test_create_user():
    body = post_test("/api/user", asdict(user1))
    try:
        with app.app_context():
            assert db.session.query(UserModel).filter(
                UserModel.uid == body["user_id"]
            ).count() == 1
    except KeyError as e:
        print(f"\n{body}\n")
        raise e


def test_create_calender():
    body = post_test("/api/calender", asdict(calender1), user1.user_token)
    try:
        calender1.calender_id = body["calender_id"]
        with app.app_context():
            assert db.session.query(CalenderModel).filter(
                CalenderModel.uid == calender1.calender_id
            ).count() == 1
    except KeyError as e:
        print(f"\n{body}\n")
        raise e


def test_delete_calender():
    body = delete_test(f"/api/calender/{calender1.calender_id}", user1.user_token)
    try:
        with app.app_context():
            assert db.session.query(CalenderModel).filter(
                CalenderModel.uid == calender1.calender_id
            ).count() == 0
    except Exception as e:
        print(f"\n{body}\n")
        raise e

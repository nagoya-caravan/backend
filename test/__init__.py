from app import app, db
from backend.json import UserJson, CalenderJson
from backend.model import CalenderModel, SharedModel, EventModel, UserModel

app.config['TESTING'] = True
client = app.test_client()

calender1 = CalenderJson(
    calender_name="calender1",
    ical_url="https://calendar.google.com/calendar/ical"
             "/6260ce613c112728eb3a58c6fc81ead067781afffbd23ec0bc09b02420f96e72%40group.calendar.google.com/private"
             "-14f0efb12610f751ac5b0f4fad5e7954/basic.ics"
)

user1 = UserJson(
    user_name="user1",
    user_token="token1"
)


def reset_db():
    with app.app_context():
        db.create_all()
        db.session.query(SharedModel).delete()
        db.session.query(EventModel).delete()
        db.session.query(CalenderModel).delete()
        db.session.query(UserModel).delete()
        db.session.commit()


def post_test(path: str, json_data: dict, token: str | None = None) -> dict:
    headers = {}
    if token is not None:
        headers["Authorization"] = token
    result = client.post(path, json=json_data, headers=headers)
    return result.get_json()


def delete_test(path: str, token: str | None = None) -> dict:
    headers = {}
    if token is not None:
        headers["Authorization"] = token
    result = client.delete(path, headers=headers)
    return result.get_json()

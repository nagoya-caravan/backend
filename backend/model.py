import datetime

from ics import Event
from ics.grammar.parse import ContentLine
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from app import db
from backend.json import EventJson, CalenderJson, UserJson
from backend.util import Hash, datetime_formatter


class BaseModel:
    __table_args__ = {"extend_existing": True}


class UserModel(BaseModel, db.Model):
    __tablename__ = "user"
    uid: int | Column = Column(Integer, primary_key=True, name="uid", autoincrement=True)
    name: str | Column = Column(String(64), nullable=False, unique=True)
    hash_token: str | Column = Column(String(128), nullable=False, unique=True)

    def apply_user_json(self, user_json: UserJson):
        self.name = user_json.user_name
        if user_json.user_token is not None:
            self.hash_token = Hash.hash(user_json.user_token)

    def to_user_json(self):
        return UserJson(
            user_id=self.uid,
            user_name=self.name,
        )


class CalenderModel(BaseModel, db.Model):
    __tablename__ = "calender"
    uid: int | Column = Column(Integer, primary_key=True, name="uid", autoincrement=True)
    user_id: int | Column = Column(ForeignKey("user.uid", ondelete="CASCADE"), nullable=False)
    name: str | Column = Column(String(16), nullable=False)
    ical_url: str | Column = Column(String(256), nullable=False)

    def apply_calender_json(self, calender_json: CalenderJson):
        if calender_json.calender_id is not None:
            self.uid = calender_json.calender_id
        self.name = calender_json.calender_name
        self.ical_url = calender_json.ical_url

    def to_calender_json(self):
        return CalenderJson(
            self.name,
            self.ical_url,
            self.uid,
        )


class SharedUserCalenderModel(BaseModel, db.Model):
    __tablename__ = "shared_user_calender"
    user_id: int | Column = Column(
        ForeignKey("user.uid", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    calender_id: int | Column = Column(
        ForeignKey("calender.uid", ondelete="CASCADE"), nullable=False, primary_key=True
    )

    def __init__(self, calender_id: int, user_id: int):
        self.calender_id = calender_id
        self.user_id = user_id


class EventModel(BaseModel, db.Model):
    __tablename__ = "event"
    uid: int | Column = Column(Integer, primary_key=True, name="uid", autoincrement=True)
    calender_id: int | Column = Column(ForeignKey("calender.uid", ondelete="CASCADE"), nullable=False)
    ical_uid: str | Column = Column(String(128), nullable=False)
    is_show: bool | Column = Column(Boolean, nullable=False)
    is_all_day: bool | Column = Column(Boolean, nullable=False)
    title: str | Column = Column(String(64), nullable=False, default="")
    description: str | None | Column = Column(String(1024), nullable=True)
    start_date: datetime.datetime | Column = Column(DateTime, nullable=False)
    end_date: datetime.datetime | Column = Column(DateTime, nullable=False)
    location: str | None | Column = Column(String(256), nullable=True)
    rrule: str | None | Column = Column(String(128), nullable=True)

    def __init__(
            self,
            calender_id: int | None = None,
            uid: str | None = None,
    ):
        if calender_id is not None:
            self.calender_id = calender_id
            self.ical_uid = uid

    def apply_ical(self, ical_event: Event):
        self.title = ical_event.name or ""
        self.description = ical_event.description
        self.start_date = ical_event.begin.datetime
        self.end_date = ical_event.end.datetime
        self.location = ical_event.location
        self.is_all_day = ical_event.all_day
        for container in ical_event.extra:
            container: ContentLine
            if container.name == "RRULE":
                self.rrule = container.value

    def to_event_json(self):
        return (EventJson(
            calender_id=self.calender_id,
            ical_uid=self.ical_uid,
            is_show=self.is_show,
            event_title=self.title,
            description=self.description,
            start=datetime_formatter.date_to_str(self.start_date),
            end=datetime_formatter.date_to_str(self.end_date),
            location=self.location,
            event_id=self.uid,
            all_day=self.is_all_day
        ))

import datetime

from ics import Event
from ics.grammar.parse import ContentLine
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from app import db
from backend.formatter import datetime_formatter
from backend.json import EventJson, CalenderJson, UserJson


class BaseModel:
    __table_args__ = {"extend_existing": True}


class UserModel(BaseModel, db.Model):
    __tablename__ = "user"
    user_id: int | Column = Column(Integer, primary_key=True, name="user_id", autoincrement=True)
    user_name: str | Column = Column(String(64), nullable=False)
    user_token: str | Column = Column(String(128), nullable=False)

    def apply_user_json(self, user_json: UserJson):
        self.user_name = user_json.user_name
        self.user_token = user_json.user_token

    def to_user_json(self):
        return UserJson(
            user_name=self.user_name,
            user_token=self.user_token,
        )


class CalenderModel(BaseModel, db.Model):
    __tablename__ = "calender"
    calender_id: int | Column = Column(Integer, primary_key=True, name="calender_id", autoincrement=True)
    calender_name: str | Column = Column(String(16), nullable=False)
    ical_url: str | Column = Column(String(256), nullable=False)

    def apply_calender_json(self, calender_json: CalenderJson):
        if calender_json.calender_id is not None:
            self.calender_id = calender_json.calender_id
        self.calender_name = calender_json.calender_name
        self.ical_url = calender_json.ical_url

    def to_calender_json(self):
        return CalenderJson(
            self.calender_name,
            self.ical_url,
            self.calender_id,
        )


class EventModel(BaseModel, db.Model):
    __tablename__ = "event"
    event_id: int | Column = Column(Integer, primary_key=True, name="event_id", autoincrement=True)
    calender_id: int | Column = Column(ForeignKey("calender.calender_id", ondelete="CASCADE"), nullable=False)
    ical_uid: str | Column = Column(String(128), nullable=False)
    is_show: bool | Column = Column(Boolean, nullable=False)
    event_title: str | Column = Column(String(64), nullable=False, default="")
    description: str | None | Column = Column(String(1024), nullable=True)
    start: datetime.datetime | Column = Column(DateTime, nullable=False)
    end: datetime.datetime | Column = Column(DateTime, nullable=False)
    location: str | None | Column = Column(String(256), nullable=True)
    rrule: str | None | Column = Column(String(128), nullable=True)
    all_day: bool | Column = Column(Boolean, nullable=False)

    def __init__(
            self,
            calender_id: int | None = None,
            uid: str | None = None,
    ):
        if calender_id is not None:
            self.calender_id = calender_id
            self.ical_uid = uid

    def apply_ical(self, ical_event: Event):
        self.event_title = ical_event.name or ""
        self.description = ical_event.description
        self.start = ical_event.begin.datetime
        self.end = ical_event.end.datetime
        self.location = ical_event.location
        self.all_day = ical_event.all_day
        for container in ical_event.extra:
            container: ContentLine
            if container.name == "RRULE":
                self.rrule = container.value

    def to_event_json(self):
        return (EventJson(
            calender_id=self.calender_id,
            ical_uid=self.ical_uid,
            is_show=self.is_show,
            event_title=self.event_title,
            description=self.description,
            start=datetime_formatter.date_to_str(self.start),
            end=datetime_formatter.date_to_str(self.end),
            location=self.location,
            event_id=self.event_id,
            all_day=self.all_day
        ))

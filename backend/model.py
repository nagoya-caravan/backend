import datetime

from ics import Event
from ics.grammar.parse import ContentLine
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from app import db
from backend.formatter import datetime_formatter
from backend.json import EventJson, CalenderJson


class BaseModel:
    __table_args__ = {"extend_existing": True}


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
    uid: str | Column = Column(String(128), nullable=False)
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
            self.uid = uid

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
            self.calender_id,
            self.uid,
            self.is_show,
            self.event_title,
            self.description,
            datetime_formatter.date_to_str(self.start),
            datetime_formatter.date_to_str(self.end),
            self.location,
            self.event_id
        ))

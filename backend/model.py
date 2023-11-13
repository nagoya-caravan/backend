import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from app import db


class BaseModel:
    __table_args__ = {"extend_existing": True}


class IcalModel(BaseModel, db.Model):
    __tablename__ = "ical_url"
    ical_id: int | Column = Column(Integer, primary_key=True, name="ical_id", autoincrement=True)
    url: str | Column = Column(String(256), nullable=False)
    calender_id: int | Column = Column(ForeignKey("calender.calender_id", ondelete="CASCADE"), nullable=False)

    def __init__(self, url: str, calender_id: int):
        self.url = url
        self.calender_id = calender_id


class CalenderModel(BaseModel, db.Model):
    __tablename__ = "calender"
    calender_id: int | Column = Column(Integer, primary_key=True, name="calender_id", autoincrement=True)
    calender_name: str | Column = Column(String(16), nullable=False)

    def __init__(self, calender_name: str | None = None):
        self.calender_name = calender_name


class EventModel(BaseModel, db.Model):
    __tablename__ = "event"
    event_id: int | Column = Column(Integer, primary_key=True, name="event_id", autoincrement=True)
    ical_id: int | Column = Column(ForeignKey("ical_url.ical_id", ondelete="CASCADE"), nullable=False)
    uid: str | Column = Column(String(128), nullable=False)
    is_show: bool | Column = Column(Boolean, nullable=False)
    event_title: str | Column = Column(String(64), nullable=False, default="")
    description: str | Column = Column(String(1024), nullable=True)
    start: datetime.datetime | Column = Column(DateTime, nullable=False)
    end: datetime.datetime | Column = Column(DateTime, nullable=False)
    location: str | Column = Column(String(256), nullable=True)

    def __init__(
            self,
            ical_url_id: int | None = None,
            uid: str | None = None,
    ):
        self.ical_id = ical_url_id
        self.uid = uid

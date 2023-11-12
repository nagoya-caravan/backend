from sqlalchemy import Column, Integer, String, ForeignKey

from app import db


class BaseModel:
    __table_args__ = {"extend_existing": True}


class IcalUrlModel(BaseModel, db.Model):
    __tablename__ = "ical_url"
    ical_id: int | Column = Column(Integer, primary_key=True, name="ical_id", autoincrement=True)
    url: str | Column = Column(String(128), nullable=False)
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

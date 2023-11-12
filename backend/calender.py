from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, ForeignKey

from app import db
from backend.error import ErrorIdException, ErrorIds
from backend.model import BaseModel


@dataclass
class CalenderJson:
    calender_name: str
    ical_urls: list[str]
    calender_id: int | None = None


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


class CalenderManager:
    @staticmethod
    def create(calender_name: str, ical_urls: list[str]):
        calender = CalenderModel(calender_name)

        db.session.add(calender)
        db.session.commit()
        for url in set(ical_urls):
            db.session.add(IcalUrlModel(url, calender.calender_id))
        db.session.commit()

        return {"calender_id": calender.calender_id}

    @staticmethod
    def edit(calender_id: int, calender_name: str, ical_urls: list[str]):

        calender: CalenderModel = db.session.query(CalenderModel).filter(
            CalenderModel.calender_id == calender_id
        ).first()

        if calender is None:
            raise ErrorIdException(ErrorIds.CALENDER_NOT_FOUND)
        calender.calender_name = calender_name

        url_models: list[IcalUrlModel] = db.session.query(IcalUrlModel).filter(
            IcalUrlModel.calender_id == calender_id
        ).all()

        for url_model in url_models:
            if url_model.url not in ical_urls:
                db.session.query(IcalUrlModel).filter(
                    IcalUrlModel.ical_id == url_model.ical_id
                ).delete()
            else:
                ical_urls.remove(url_model.url)

        for url in ical_urls:
            db.session.add(IcalUrlModel(url, calender_id))

        db.session.commit()

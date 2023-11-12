from app import db
from backend.repository import CalenderRepository


class IcalUrlManager:
    pass


class CalenderManager:

    @staticmethod
    def create(calender_name: str, ical_urls: list[str]):
        result = CalenderRepository.create(calender_name, ical_urls)
        db.session.commit()
        return result

    @staticmethod
    def edit(calender_id: int, calender_name: str, ical_urls: list[str]):
        CalenderRepository.edit(calender_id, calender_name, ical_urls)
        db.session.commit()

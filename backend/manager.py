from app import db
from backend.json import CalenderIdJson, CalenderJson
from backend.repository import CalenderRepository, IcalUrlRepository


class CalenderManager:
    @staticmethod
    def get(calender_id: int):
        calender_model = CalenderRepository.get_model(calender_id)
        ical_models = IcalUrlRepository.get_models(calender_id)
        ical_urls = list()
        for model in ical_models:
            ical_urls.append(model.url)
        return CalenderJson(calender_model.calender_name, ical_urls, calender_id)

    @staticmethod
    def create(calender_name: str, ical_urls: list[str]):
        result = CalenderRepository.create(calender_name)
        IcalUrlRepository.save(result.calender_id, ical_urls)
        db.session.commit()
        return CalenderIdJson(result.calender_id)

    @staticmethod
    def edit(calender_id: int, calender_name: str, ical_urls: list[str]):
        CalenderRepository.edit(calender_id, calender_name)
        IcalUrlRepository.save(calender_id, ical_urls)
        db.session.commit()
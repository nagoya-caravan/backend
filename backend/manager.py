from app import db
from backend.json import CalenderIdJson, CalenderJson, EventEditJson
from backend.model import CalenderModel
from backend.repository import CalenderRepository, IcalUrlRepository, EventRepository


class IcalUrlManager:
    @staticmethod
    def get_urls(calender_id: int) -> list[str]:
        ical_models = IcalUrlRepository.get_models(calender_id)
        ical_urls = list()
        for model in ical_models:
            ical_urls.append(model.url)
        return ical_urls


class CalenderManager:
    @staticmethod
    def get_list(page: int, size: int):
        models = CalenderRepository.get_list(page, size)
        jsons = list[CalenderJson]()
        for model in models:
            jsons.append(CalenderJson(
                model.calender_name,
                IcalUrlManager.get_urls(model.ical_id),
                model.ical_id
            ))
        return jsons

    @staticmethod
    def get(calender_id: int):
        calender_model = CalenderRepository.get_model(calender_id)
        return CalenderJson(
            calender_model.calender_name,
            IcalUrlManager.get_urls(calender_id),
            calender_id
        )

    @staticmethod
    def create(calender_name: str, ical_urls: list[str]):
        result: CalenderModel = CalenderRepository.create(calender_name)
        IcalUrlRepository.save(result.calender_id, ical_urls)
        db.session.commit()
        return CalenderIdJson(result.calender_id)

    @staticmethod
    def edit(calender_id: int, calender_name: str, ical_urls: list[str]):
        CalenderRepository.edit(calender_id, calender_name)
        IcalUrlRepository.save(calender_id, ical_urls)
        db.session.commit()


class EventManager:
    @staticmethod
    def refresh(calender_id: int):
        url_models = IcalUrlRepository.get_models(calender_id)
        for url_model in url_models:
            EventRepository.refresh_ical_url(url_model.ical_id, url_model.url)
        db.session.commit()

    @staticmethod
    def edit(event_id: int, event_edit: EventEditJson):
        EventRepository.edit(event_id, event_edit.is_show)
        db.session.commit()

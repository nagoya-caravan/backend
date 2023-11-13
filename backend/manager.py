import datetime

from dateutil.rrule import rrulestr

from app import db
from backend.formatter import datetime_formatter
from backend.json import CalenderIdJson, CalenderJson, EventEditJson, EventJson
from backend.model import CalenderModel
from backend.repository import CalenderRepository, EventRepository


class CalenderManager:
    @staticmethod
    def get_list(page: int, size: int):
        models = CalenderRepository.get_list(page, size)
        jsons = list[CalenderJson]()
        for model in models:
            jsons.append(model.to_calender_json())
        return jsons

    @staticmethod
    def get(calender_id: int):
        calender_model = CalenderRepository.get_model(calender_id)
        return calender_model.to_calender_json()

    @staticmethod
    def create(calender_json: CalenderJson):
        result: CalenderModel = CalenderRepository.create(calender_json)
        db.session.commit()
        return CalenderIdJson(result.calender_id)

    @staticmethod
    def edit(calender_json: CalenderJson):
        CalenderRepository.edit(calender_json)
        db.session.commit()


class EventManager:
    @staticmethod
    def refresh(calender_id: int):
        EventRepository.refresh_calender_id(calender_id)
        db.session.commit()

    @staticmethod
    def edit(event_id: int, event_edit: EventEditJson):
        EventRepository.edit(event_id, event_edit.is_show)
        db.session.commit()

    @staticmethod
    def event_by_calender(
            calender_id: int,
            start: datetime.datetime,
            end: datetime.datetime,
            timezone: datetime.timezone,
    ):
        return EventManager.event_by_ical(
            calender_id, start, end, timezone
        )

    @staticmethod
    def event_by_ical(
            calender_id: int,
            start: datetime.datetime,
            end: datetime.datetime,
            timezone: datetime.timezone,
    ):
        models = EventRepository.get_list(calender_id)
        jsons = list[EventJson]()

        for model in models:
            model_start = model.start.astimezone()
            model_end = model.end.astimezone()
            if not (end < model_start or model_end < start):
                jsons.append(model.to_event_json())
                continue
            rrule_str = model.rrule
            if rrule_str is None:
                continue
            rrule = rrulestr(rrule_str)
            for start_time in rrule:
                end_date = start_time.date() + (model_end.date() - model_start.date())
                start_time = start_time.replace(
                    hour=model_start.hour, minute=model_start.minute, second=model_start.second,
                    microsecond=model_start.microsecond, tzinfo=model_start.tzinfo
                )
                end_time = datetime.datetime(
                    year=end_date.year, month=end_date.month, day=end_date.day,
                    hour=model_end.hour, minute=model_end.minute, second=model_end.second,
                    microsecond=model_end.microsecond, tzinfo=model_end.tzinfo
                )
                if end_time < start:
                    continue
                if end < start_time:
                    break
                event_json = model.to_event_json()
                event_json.start = datetime_formatter.date_to_str(start_time.astimezone(timezone))
                event_json.end = datetime_formatter.date_to_str(end_time.astimezone(timezone))
                jsons.append(event_json)

        return jsons

from dateutil.rrule import rrulestr

from app import db
from backend.formatter import datetime_formatter
from backend.json import CalenderIdJson, CalenderJson, EventEditJson, EventJson, UserJson, UserIdJson
from backend.model import CalenderModel, UserModel
from backend.repository import CalenderRepository, EventRepository, UserRepository
from backend.util import DatetimeRange


class UserManager:

    @staticmethod
    def create(user_json: UserJson):
        result: UserModel = UserRepository.create(user_json)
        db.session.commit()
        return UserIdJson(result.calender_id)


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
            datetime_range: DatetimeRange,
    ):
        return EventManager.event_by_ical(
            calender_id, datetime_range
        )

    @staticmethod
    def public_event_by_calender(
            calender_id: int,
            datetime_range: DatetimeRange
    ):
        result = list[EventJson]()
        for event in EventManager.event_by_calender(calender_id, datetime_range):
            if event.is_show:
                result.append(event)
                continue
            result.append(EventJson(
                event.calender_id, event.is_show, event.start, event.end, None, None, None, None,
            ))
        return result

    @staticmethod
    def event_by_ical(
            calender_id: int,
            check_range: DatetimeRange,
    ):
        models = EventRepository.get_list(calender_id)
        jsons = list[EventJson]()

        for model in models:
            model_range = DatetimeRange(model.start, model.end)

            if check_range.is_overlap(model_range):
                jsons.append(model.to_event_json())
                continue
            rrule_str = model.rrule
            if rrule_str is None:
                continue
            rrule = rrulestr(rrule_str, dtstart=model_range.start.astimezone())
            for start_time in rrule:
                end_time = start_time + model_range.during()

                if end_time < check_range.start.astimezone():
                    continue
                if check_range.end.astimezone() < start_time:
                    break
                event_json = model.to_event_json()
                event_json.start = datetime_formatter.date_to_str(start_time)
                event_json.end = datetime_formatter.date_to_str(end_time)
                jsons.append(event_json)

        return jsons

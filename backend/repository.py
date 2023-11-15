from http import client
from urllib import request

import ics
from ics import Event

from app import db
from backend.error import ErrorIdException, ErrorIds
from backend.json import CalenderJson, UserJson
from backend.model import CalenderModel, EventModel, UserModel


class UserRepository:

    @staticmethod
    def create(user_json: UserJson):
        model = UserModel()
        model.apply_user_json(user_json)
        db.session.add(model)
        return model


class CalenderRepository:
    @staticmethod
    def get_list(page: int, size: int):
        return db.session.query(CalenderModel).offset(page * size).limit(size).all()

    @staticmethod
    def get_model_ornone(calender_id: int) -> CalenderModel | None:
        return db.session.query(CalenderModel).filter(
            CalenderModel.calender_id == calender_id
        ).first()

    @staticmethod
    def get_model(calender_id: int) -> CalenderModel:
        result = CalenderRepository.get_model_ornone(calender_id)
        if result is None:
            raise ErrorIdException(ErrorIds.CALENDER_NOT_FOUND)
        return result

    @staticmethod
    def create(calender_json: CalenderJson):
        calender_model = CalenderModel()
        calender_model.apply_calender_json(calender_json)
        db.session.add(calender_model)
        db.session.commit()
        EventRepository.refresh_ical(calender_model)
        return calender_model

    @staticmethod
    def edit(calender_json: CalenderJson):
        calender_model = CalenderRepository.get_model(calender_json.calender_id)
        calender_model.apply_calender_json(calender_model)
        EventRepository.refresh_ical(calender_model)
        return calender_model


class EventRepository:
    @staticmethod
    def get_events(calender_id: int) -> list[EventModel]:
        return db.session.query(EventModel).filter(
            EventModel.calender_id == calender_id
        ).all()

    @staticmethod
    def refresh_calender_id(calender_id: int):
        EventRepository.refresh_ical(CalenderRepository.get_model(calender_id))

    @staticmethod
    def refresh_ical(calender_model: CalenderModel):
        try:
            with request.urlopen(request.Request(calender_model.ical_url)) as response:
                response: client.HTTPResponse
                ical_text = response.read().decode("utf-8")
        except ValueError:
            print(calender_model.ical_url)
            raise ErrorIdException(ErrorIds.ICAL_URL_NOT_VALID)
        try:
            ical = ics.Calendar(ical_text)
        except TypeError:
            print(ical_text)
            raise ErrorIdException(ErrorIds.ICAL_TXT_NOT_VALID)
        EventRepository.refresh_ical_event(calender_model, ical.events)

    @staticmethod
    def refresh_ical_event(calender_model: CalenderModel, ical_events: set[Event]):
        event_models = EventRepository.get_events(calender_model.calender_id)
        edited_models = list[EventModel]()

        for event_model in event_models:
            event = EventRepository.ical_event_by_uid(ical_events, event_model.ical_uid)
            if event is None:
                db.session.query(EventModel).filter(
                    EventModel.event_id == event_model.event_id
                ).delete()
            else:
                edited_models.append(event_model)
                event_model.apply_ical(event)
                ical_events.remove(event)

        for event in ical_events:
            new_model = EventModel(
                calender_id=calender_model.calender_id,
                uid=event.uid
            )
            new_model.apply_ical(event)
            new_model.is_show = False

            edited_models.append(new_model)
            db.session.add(new_model)

    @staticmethod
    def ical_event_by_uid(ical_events: set[Event], uid: str):
        for event in ical_events:
            if event.uid == uid:
                return event
        return None

    @staticmethod
    def edit(event_id: int, is_show: bool):
        event = EventRepository.get_model(event_id)
        event.is_show = is_show
        return event

    @staticmethod
    def get_model(event_id: int):
        result = EventRepository.get_model_ornone(event_id)
        if result is None:
            raise ErrorIdException(ErrorIds.EVENT_NOT_FOUND)
        return result

    @staticmethod
    def get_model_ornone(event_id: int) -> EventModel | None:
        return db.session.query(EventModel).filter(
            EventModel.event_id == event_id
        ).first()

    @staticmethod
    def get_list(ical_id: int) -> list[EventModel]:
        return db.session.query(EventModel).filter(
            EventModel.calender_id == ical_id,
        ).all()

from http import client
from urllib import request

import flask
import ics
from ics import Event

from app import db
from backend.error import ErrorIdException, ErrorIds
from backend.json import CalenderJson, UserJson
from backend.model import CalenderModel, EventModel, UserModel
from backend.util import Hash


class UserRepository:

    @staticmethod
    def get_model_ornone(user_id: int) -> UserModel | None:
        return db.session.query(UserModel).filter(
            UserModel.uid == user_id
        ).first()

    @staticmethod
    def model_by_header_ornone() -> UserModel | None:
        token = flask.request.headers.get("Authorization", None)
        if token is None:
            return None
        return db.session.query(UserModel).filter(
            UserModel.hash_token == Hash.hash(token)
        ).first()

    @staticmethod
    def model_by_header():
        result = UserRepository.model_by_header_ornone()
        if result is None:
            raise ErrorIdException(ErrorIds.USER_NOT_FOUND)
        return result

    @staticmethod
    def get_model(user_id: int):
        result = UserRepository.get_model_ornone(user_id)
        if result is None:
            raise ErrorIdException(ErrorIds.USER_NOT_FOUND)
        return result

    @staticmethod
    def count_by_name(user_name: str):
        return db.session.query(UserModel).filter(
            UserModel.name == user_name
        ).count()

    @staticmethod
    def create(user_json: UserJson):
        if UserRepository.count_by_name(user_json.user_name) != 0:
            raise ErrorIdException(ErrorIds.USER_NAME_CONFLICT)
        model = UserModel()
        model.apply_user_json(user_json)
        db.session.add(model)
        return model

    @staticmethod
    def edit(user_json: UserJson):
        model = UserRepository.model_by_header()
        model.apply_user_json(user_json)
        return model


class CalenderRepository:
    @staticmethod
    def get_list(user_model: UserModel, page: int, size: int):
        return db.session.query(CalenderModel).filter(
            CalenderModel.user_id == user_model.uid
        ).offset(page * size).limit(size).all()

    @staticmethod
    def self_model_ornone(calender_id: int) -> CalenderModel | None:
        user = UserRepository.model_by_header_ornone()
        if user is None:
            return None
        return db.session.query(CalenderModel).filter(
            CalenderModel.uid == calender_id,
            CalenderModel.user_id == user.uid
        ).first()

    @staticmethod
    def self_model(calender_id: int) -> CalenderModel:
        result = CalenderRepository.self_model_ornone(calender_id)
        if result is None:
            raise ErrorIdException(ErrorIds.CALENDER_NOT_FOUND)
        return result

    @staticmethod
    def create(user_model: UserModel, calender_json: CalenderJson):
        calender_model = CalenderModel()
        calender_model.user_id = user_model.uid
        calender_model.apply_calender_json(calender_json)
        db.session.add(calender_model)
        db.session.commit()
        EventRepository.refresh_ical(calender_model)
        return calender_model

    @staticmethod
    def edit(calender_json: CalenderJson):
        calender_model = CalenderRepository.self_model(calender_json.calender_id)
        calender_model.apply_calender_json(calender_model)
        EventRepository.refresh_ical(calender_model)
        return calender_model


def ical_event_by_uid(ical_events: set[Event], uid: str):
    for event in ical_events:
        if event.uid == uid:
            return event
    return None


class EventRepository:
    @staticmethod
    def get_events(calender_model: CalenderModel) -> list[EventModel]:
        return db.session.query(EventModel).filter(
            EventModel.calender_id == calender_model.uid
        ).all()

    @staticmethod
    def refresh_calender(calender_model: CalenderModel):
        EventRepository.refresh_ical(calender_model)

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
        event_models = EventRepository.get_events(calender_model)
        edited_models = list[EventModel]()

        for event_model in event_models:
            event = ical_event_by_uid(ical_events, event_model.ical_uid)
            if event is None:
                db.session.query(EventModel).filter(
                    EventModel.uid == event_model.uid
                ).delete()
            else:
                edited_models.append(event_model)
                event_model.apply_ical(event)
                ical_events.remove(event)

        for event in ical_events:
            new_model = EventModel(
                calender_id=calender_model.uid,
                uid=event.uid
            )
            new_model.apply_ical(event)
            new_model.is_show = False

            edited_models.append(new_model)
            db.session.add(new_model)

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
            EventModel.uid == event_id
        ).first()

    @staticmethod
    def get_list(ical_id: int) -> list[EventModel]:
        return db.session.query(EventModel).filter(
            EventModel.calender_id == ical_id,
        ).all()

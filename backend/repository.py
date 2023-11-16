from http import client
from urllib import request

import flask
import ics
from ics import Event
from sqlalchemy import or_, and_

from app import db
from backend.error import ErrorIdException, ErrorIds
from backend.json import CalenderJson, UserJson, ShareJson
from backend.model import CalenderModel, EventModel, UserModel, SharedUserCalenderModel
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
    def model_by_id_ornone(user_id: int) -> UserModel | None:
        return db.session.query(UserModel).filter(
            UserModel.uid == user_id
        ).first()

    @staticmethod
    def model_by_header():
        result = UserRepository.model_by_header_ornone()
        if result is None:
            raise ErrorIdException(ErrorIds.USER_NOT_FOUND)
        return result

    @staticmethod
    def model_by_id(user_id: int):
        result = UserRepository.model_by_id_ornone(user_id)
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
    def count_by_token(hash_token: str):
        return db.session.query(UserModel).filter(
            UserModel.hash_token == hash_token
        ).count()

    @staticmethod
    def create(user_json: UserJson):
        if UserRepository.count_by_name(user_json.user_name) != 0:
            raise ErrorIdException(ErrorIds.USER_NAME_CONFLICT)
        if UserRepository.count_by_token(Hash.hash(user_json.user_token)) != 0:
            raise ErrorIdException(ErrorIds.TOKEN_CONFLICT)
        model = UserModel()
        model.apply_user_json(user_json)
        db.session.add(model)
        return model

    @staticmethod
    def edit(user_json: UserJson):
        model = UserRepository.model_by_header()
        if db.session.query(UserModel).filter(
                UserModel.uid != model.uid,
                UserModel.name == user_json.user_name
        ).count() != 0:
            raise ErrorIdException(ErrorIds.USER_NAME_CONFLICT)
        if db.session.query(UserModel).filter(
                UserModel.uid != model.uid,
                UserModel.hash_token == Hash.hash(user_json.user_token)
        ).count() != 0:
            raise ErrorIdException(ErrorIds.TOKEN_CONFLICT)
        model.apply_user_json(user_json)
        return model


class CalenderRepository:
    @staticmethod
    def get_list(user_model: UserModel, page: int, size: int):
        return db.session.query(CalenderModel).filter(
            CalenderModel.user_id == user_model.uid
        ).offset(page * size).limit(size).all()

    @staticmethod
    def self_model_ornone(user_model: UserModel, calender_id: int) -> CalenderModel | None:
        return db.session.query(CalenderModel).filter(
            CalenderModel.uid == calender_id,
            CalenderModel.user_id == user_model.uid
        ).first()

    @staticmethod
    def readable_model_by_user_id(user_model: UserModel, calender_id: int) -> CalenderModel:
        result = db.session.query(CalenderModel).outerjoin(
            SharedUserCalenderModel,
            SharedUserCalenderModel.calender_id == CalenderModel.uid
        ).filter(
            CalenderModel.uid == calender_id,
            or_(
                and_(
                    CalenderModel.uid == SharedUserCalenderModel.calender_id,
                    SharedUserCalenderModel.user_id == user_model.uid
                ),
                CalenderModel.user_id == user_model.uid,
            )
        ).first()
        if result is None:
            raise ErrorIdException(ErrorIds.CALENDER_NOT_FOUND)
        return result

    @staticmethod
    def model_by_user_id(user_model: UserModel, calender_id: int) -> CalenderModel:
        result = CalenderRepository.self_model_ornone(user_model, calender_id)
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
    def edit(user_model: UserModel, calender_json: CalenderJson):
        calender_model = CalenderRepository.model_by_user_id(user_model, calender_json.calender_id)
        calender_model.apply_calender_json(calender_json)
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
    def edit(user_model: UserModel, event_id: int, is_show: bool):
        event = EventRepository.model_by_user_id(user_model, event_id)
        event.is_show = is_show
        return event

    @staticmethod
    def model_by_user_id(user_model: UserModel, event_id: int):
        result = EventRepository.model_by_user_id_ornone(user_model, event_id)
        if result is None:
            raise ErrorIdException(ErrorIds.EVENT_NOT_FOUND)
        return result

    @staticmethod
    def model_by_user_id_ornone(user_model: UserModel, event_id: int) -> EventModel | None:
        return db.session.query(EventModel).filter(
            EventModel.uid == event_id,
            EventModel.calender_id == CalenderModel.uid,
            CalenderModel.user_id == user_model.uid
        ).first()

    @staticmethod
    def models_by_calender(calender_model: CalenderModel) -> list[EventModel]:
        return db.session.query(EventModel).filter(
            EventModel.calender_id == calender_model.uid
        ).all()


class ShareRepository:
    @staticmethod
    def save_share(calender_model: CalenderModel, share_json: ShareJson):
        share_models: list[SharedUserCalenderModel] = ShareRepository.models(calender_model)
        edited_models = list[SharedUserCalenderModel]()
        new_users = [*share_json.user_ids]

        for share_model in share_models:
            if share_json.user_ids not in new_users:
                db.session.query(SharedUserCalenderModel).filter(
                    SharedUserCalenderModel.user_id == share_model.user_id,
                    SharedUserCalenderModel.calender_id == share_model.calender_id
                ).delete()
            else:
                edited_models.append(share_model)
                new_users.remove(share_model.user_id)

        for user_id in new_users:
            new_model = SharedUserCalenderModel(
                calender_id=calender_model.uid,
                user_id=user_id
            )
            edited_models.append(new_model)
            db.session.add(new_model)
        return edited_models

    @staticmethod
    def models(calender_model: CalenderModel) -> list[SharedUserCalenderModel]:
        return db.session.query(SharedUserCalenderModel).filter(
            SharedUserCalenderModel.calender_id == calender_model.uid
        ).all()

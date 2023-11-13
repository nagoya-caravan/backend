import datetime
from http import client
from urllib import request

import ics
from ics import Event
from sqlalchemy import or_, and_

from app import db
from backend.error import ErrorIdException, ErrorIds
from backend.model import IcalModel, CalenderModel, EventModel


class IcalRepository:

    @staticmethod
    def get_models(calender_id: int) -> list[IcalModel]:
        return db.session.query(IcalModel).filter(
            IcalModel.calender_id == calender_id
        ).all()

    @staticmethod
    def get_model_ornone(ical_url_id: int) -> IcalModel | None:
        return db.session.query(IcalModel).filter(
            IcalModel.ical_url_id == ical_url_id
        ).first()

    @staticmethod
    def get_model(ical_url_id: int) -> IcalModel:
        result = IcalRepository.get_model_ornone(ical_url_id)
        if result is None:
            raise ErrorIdException(ErrorIds.CALENDER_NOT_FOUND)
        return result

    @staticmethod
    def save(calender_id: int, ical_urls: list[str]):
        url_models = IcalRepository.get_models(calender_id)
        ical_urls = set(ical_urls)
        edited_models = list[IcalModel]()

        for url_model in url_models:
            if url_model.url not in ical_urls:
                db.session.query(IcalModel).filter(
                    IcalModel.ical_id == url_model.ical_id
                ).delete()
            else:
                edited_models.append(url_model)
                ical_urls.remove(url_model.url)

        for url in ical_urls:
            new_model = IcalModel(url, calender_id)
            edited_models.append(new_model)
            db.session.add(new_model)
            db.session.commit()
            EventRepository.refresh_ical_url(new_model.ical_id, url)

        return edited_models


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
    def create(calender_name: str):
        calender = CalenderModel(calender_name)
        db.session.add(calender)
        db.session.commit()
        return calender

    @staticmethod
    def edit(calender_id: int, calender_name: str):
        calender = CalenderRepository.get_model(calender_id)
        calender.calender_name = calender_name
        return calender


class EventRepository:
    @staticmethod
    def get_events(ical_url_id: int) -> list[EventModel]:
        return db.session.query(EventModel).filter(
            EventModel.ical_id == ical_url_id
        ).all()

    @staticmethod
    def refresh_ical_url(ical_url_id: int, url: str):
        with request.urlopen(request.Request(url)) as response:
            response: client.HTTPResponse
            ical_text = response.read().decode("utf-8")
        try:
            ical = ics.Calendar(ical_text)
        except TypeError:
            print(ical_text)
            raise ErrorIdException(ErrorIds.ICAL_NOT_VALID)
        EventRepository.refresh_ical_event(ical_url_id, ical.events)

    @staticmethod
    def refresh_ical_event(ical_url_id: int, ical_events: set[Event]):
        event_models = EventRepository.get_events(ical_url_id)
        edited_models = list[EventModel]()

        for event_model in event_models:
            event = EventRepository.ical_event_by_uid(ical_events, event_model.uid)
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
                ical_url_id,
                event.uid
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
            raise ErrorIdException(ErrorIds.CALENDER_NOT_FOUND)
        return result

    @staticmethod
    def get_model_ornone(event_id: int) -> EventModel | None:
        return db.session.query(EventModel).filter(
            EventModel.event_id == event_id
        ).first()

    @staticmethod
    def get_list(ical_id: int, start: datetime.datetime, end: datetime.datetime) -> list[EventModel]:
        return db.session.query(EventModel).filter(
            EventModel.ical_id == ical_id,
            or_(
                and_(
                    EventModel.start <= start,
                    EventModel.end >= start
                ),
                and_(
                    EventModel.start <= end,
                    EventModel.end >= end
                ),
                and_(
                    EventModel.start <= start,
                    EventModel.end >= end
                )
            )
        ).all()

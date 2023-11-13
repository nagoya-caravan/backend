from http import client
from urllib import request

import ics
from ics import Event

from app import db
from backend.error import ErrorIdException, ErrorIds
from backend.model import IcalUrlModel, CalenderModel, EventModel


class IcalUrlRepository:

    @staticmethod
    def get_models(calender_id: int) -> list[IcalUrlModel]:
        return db.session.query(IcalUrlModel).filter(
            IcalUrlModel.calender_id == calender_id
        ).all()

    @staticmethod
    def get_model_ornone(ical_url_id: int) -> IcalUrlModel | None:
        return db.session.query(IcalUrlModel).filter(
            IcalUrlModel.ical_url_id == ical_url_id
        ).first()

    @staticmethod
    def get_model(ical_url_id: int) -> IcalUrlModel:
        result = IcalUrlRepository.get_model_ornone(ical_url_id)
        if result is None:
            raise ErrorIdException(ErrorIds.CALENDER_NOT_FOUND)
        return result

    @staticmethod
    def save(calender_id: int, ical_urls: list[str]):
        url_models = IcalUrlRepository.get_models(calender_id)
        ical_urls = set(ical_urls)
        edited_models = list[IcalUrlModel]()

        for url_model in url_models:
            if url_model.url not in ical_urls:
                db.session.query(IcalUrlModel).filter(
                    IcalUrlModel.ical_id == url_model.ical_id
                ).delete()
            else:
                edited_models.append(url_model)
                ical_urls.remove(url_model.url)

        for url in ical_urls:
            new_model = IcalUrlModel(url, calender_id)
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
            EventModel.ical_url_id == ical_url_id
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
            event = EventRepository.get_event_by_uid(ical_events, event_model.uid)
            if event is None:
                db.session.query(EventModel).filter(
                    EventModel.event_id == event_model.event_id
                ).delete()
            else:
                edited_models.append(event_model)
                event_model.event_title = event.name or ""
                event_model.description = event.description
                event_model.start = event.begin.datetime
                event_model.end = event.end.datetime
                event_model.location = event.location
                ical_events.remove(event)

        for event in ical_events:
            new_model = EventModel(
                ical_url_id,
                event.uid
            )
            new_model.event_title = event.name or ""
            new_model.description = event.description
            new_model.start = event.begin.datetime
            new_model.end = event.end.datetime
            new_model.location = event.location
            new_model.is_show = False

            edited_models.append(new_model)
            db.session.add(new_model)

    @staticmethod
    def get_event_by_uid(ical_events: set[Event], uid: str):
        for event in ical_events:
            if event.uid == uid:
                return event
        return None

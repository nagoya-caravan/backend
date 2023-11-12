from app import db
from backend.error import ErrorIdException, ErrorIds
from backend.model import IcalUrlModel, CalenderModel


class IcalUrlRepository:

    @staticmethod
    def save(calender_id: int, ical_urls: list[str]):
        url_models: list[IcalUrlModel] = db.session.query(IcalUrlModel).filter(
            IcalUrlModel.calender_id == calender_id
        ).all()

        for url_model in url_models:
            if url_model.url not in ical_urls:
                db.session.query(IcalUrlModel).filter(
                    IcalUrlModel.ical_id == url_model.ical_id
                ).delete()
            else:
                ical_urls.remove(url_model.url)

        for url in ical_urls:
            db.session.add(IcalUrlModel(url, calender_id))


class CalenderRepository:
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
    def create(calender_name: str, ical_urls: list[str]):
        calender = CalenderModel(calender_name)

        db.session.add(calender)
        db.session.commit()
        for url in set(ical_urls):
            db.session.add(IcalUrlModel(url, calender.calender_id))
        db.session.commit()

        return {"calender_id": calender.calender_id}

    @staticmethod
    def edit(calender_id: int, calender_name: str, ical_urls: list[str]):

        calender: CalenderModel = CalenderRepository.get_model(calender_id)

        calender.calender_name = calender_name

        IcalUrlRepository.save(calender_id, ical_urls)

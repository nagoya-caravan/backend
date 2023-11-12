from app import db
from backend.error import ErrorIdException, ErrorIds
from backend.model import IcalUrlModel, CalenderModel


class IcalUrlRepository:

    @staticmethod
    def get_models(calender_id: int) -> list[IcalUrlModel]:
        return db.session.query(IcalUrlModel).filter(
            IcalUrlModel.calender_id == calender_id
        ).all()

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

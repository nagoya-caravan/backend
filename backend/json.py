from dataclasses import dataclass


@dataclass
class CalenderIdJson:
    calender_id: int


@dataclass
class UserIdJson:
    user_id: int


@dataclass
class UserJson:
    user_name: str
    user_id: int | None = None
    user_token: str | None = None


@dataclass
class CalenderJson:
    calender_name: str
    ical_url: str
    user_id: int | None = None
    calender_id: int | None = None


@dataclass
class EventJson:
    calender_id: int
    is_show: bool
    start: str
    end: str
    all_day: bool
    ical_uid: str | None
    event_title: str | None
    description: str | None
    location: str | None
    event_id: int | None = None


@dataclass
class EventEditJson:
    is_show: bool


@dataclass
class ShareJson:
    calender_id: int
    user_ids: list[int]

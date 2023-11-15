from dataclasses import dataclass


@dataclass
class CalenderIdJson:
    calender_id: int


@dataclass
class UserIdJson:
    user_id: int


@dataclass
class UserJson:
    user_id: int
    user_name: str
    user_token: str | None = None


@dataclass
class CalenderJson:
    calender_name: str
    ical_url: str
    calender_id: int | None = None


@dataclass
class EventJson:
    calender_id: int
    is_show: bool
    start: str
    end: str
    ical_uid: str | None
    event_title: str | None
    description: str | None
    location: str | None
    event_id: int | None = None
    all_day: bool = False


@dataclass
class EventEditJson:
    is_show: bool

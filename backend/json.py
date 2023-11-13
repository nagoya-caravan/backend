from dataclasses import dataclass


@dataclass
class CalenderIdJson:
    calender_id: int


@dataclass
class CalenderJson:
    calender_name: str
    ical_url: str
    calender_id: int | None = None


@dataclass
class EventJson:
    ical_id: int
    ical_uid: str
    is_show: bool
    event_title: str | None
    description: str | None
    start: str | None
    end: str | None
    location: str | None
    event_id: int | None = None


@dataclass
class EventEditJson:
    is_show: bool

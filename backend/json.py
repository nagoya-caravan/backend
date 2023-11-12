from dataclasses import dataclass


@dataclass
class CalenderIdJson:
    calender_id: int


@dataclass
class CalenderJson:
    calender_name: str
    ical_urls: list[str]
    calender_id: int | None = None


@dataclass
class Event:
    event_id: int
    calender_id: int
    is_show: bool
    event_title: str | None
    description: str | None
    start: str | None
    end: str | None
    location: str | None

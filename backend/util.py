import datetime
import enum
from typing import Self


class Week(enum.Enum):
    SUNDAY = "sun",
    MONDAY = "mon",
    TUESDAY = "tue",
    WEDNESDAY = "wed",
    THURSDAY = "thu",
    FRIDAY = "fry",
    SATURDAY = "sat"


class DatetimeRange:
    def __init__(self, start: datetime.datetime, end: datetime.datetime):
        if start > end:
            raise ValueError()
        self.start = start
        self.end = end

    def is_overlap(self, other: Self):
        return not (self.end < other.start or other.end < self.start)

    def during(self):
        return self.end - self.start

import datetime
import enum
import hashlib
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


class Hash:
    """hashを扱うクラス
    """

    @staticmethod
    def hash(value: any) -> str:
        """hashを行う
        """
        return hashlib.sha512(str(value).encode("utf-8")).hexdigest()


class DatetimeFormatter:
    """日付のフォーマットを行うクラス
    :var format: 日付のフォーマット
    """
    format: str

    def __init__(self, default_format: str = "%Y-%m-%d-%H-%M-%S"):
        self.format = default_format

    def str_to_date(self, str_datetime: str) -> datetime.datetime:
        """文字列をdateに変換します
        :param str_datetime: 日付を表す文字列
        :return: date型で表される日付
        """
        return datetime.datetime.strptime(str_datetime, self.format)

    def date_to_str(self, datetime_: datetime.datetime) -> str:
        """dateを文字列に変換します
        :param datetime_: 変換する日付
        :return: フォーマットされた日付
        """
        return datetime_.strftime(self.format)


datetime_formatter = DatetimeFormatter()

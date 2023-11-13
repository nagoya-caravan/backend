import datetime


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

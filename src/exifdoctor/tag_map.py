import datetime


EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def parse_datetime(datetime_raw: str):
    return datetime.datetime.strptime(datetime_raw, EXIF_DATETIME_FORMAT)


def format_datetime(datetime: datetime.datetime):
    return datetime.strftime(EXIF_DATETIME_FORMAT)


def parse_timezone(tzinfo: str):
    hours, minutes = tzinfo[1:].split(":")
    offset = datetime.timedelta(hours=int(hours), minutes=int(minutes))

    if tzinfo[0] == "-":
        offset = -offset

    return datetime.timezone(offset)


def passthrough(data: str) -> str:
    return data


TAG_MAP = {
    "DateTimeOriginal": parse_datetime,
    "OffsetTimeOriginal": parse_timezone,
    "DateTimeDigitized": parse_datetime,
    "OffsetTimeDigitized": parse_timezone
}


def transform_tag(tag: str, value: str) -> str:
    return TAG_MAP.get(tag, passthrough)(value)

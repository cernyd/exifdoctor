import datetime
from typing import Any


EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"
EXIF_DATETIME_FORMAT_SUBSEC = "%Y:%m:%d %H:%M:%S.%f"
EXIF_TIME_FORMAT = "%H:%M:%S"


def parse_time(time_raw: str):
    return datetime.datetime.strptime(time_raw, EXIF_TIME_FORMAT)


def parse_time_with_timezone(time_raw: str):
    tz_start = -6
    time = parse_time(time_raw[:tz_start]).time()
    timezone = parse_timezone(time_raw[tz_start:])
    time.replace(tzinfo=timezone)
    return time


def parse_datetime(datetime_raw: str):
    return datetime.datetime.strptime(datetime_raw, EXIF_DATETIME_FORMAT)


def parse_datetime_subsec(datetime_raw: str):
    return datetime.datetime.strptime(datetime_raw, EXIF_DATETIME_FORMAT_SUBSEC)


def format_datetime(datetime: datetime.datetime):
    return datetime.strftime(EXIF_DATETIME_FORMAT)


def parse_datetime_with_timezone(datetime_raw: str):
    tz_start = -6
    date = parse_datetime(datetime_raw[:tz_start])
    timezone = parse_timezone(datetime_raw[tz_start:])
    date.replace(tzinfo=timezone)
    return date


def parse_datetime_subsec_with_timezone(datetime_raw: str):
    tz_start = -6
    date = parse_datetime_subsec(datetime_raw[:tz_start])
    timezone = parse_timezone(datetime_raw[tz_start:])
    date.replace(tzinfo=timezone)
    return date


def parse_datetime_any(datetime_raw: str):
    match len(datetime_raw):
        case 25:
            return parse_datetime_with_timezone(datetime_raw)
        case 19:
            return parse_datetime(datetime_raw)
        case _:
            return parse_datetime_subsec_with_timezone(datetime_raw)


def parse_timezone(tzinfo: str):
    hours, minutes = tzinfo[1:].split(":")
    offset = datetime.timedelta(hours=int(hours), minutes=int(minutes))

    if tzinfo[0] == "-":
        offset = -offset

    return datetime.timezone(offset)


def passthrough(data: str) -> str:
    return data


TAG_MAP = {
    "DateTimeOriginal": parse_datetime_any,
    "OffsetTimeOriginal": parse_timezone,
    "DateTimeDigitized": parse_datetime,
    "OffsetTimeDigitized": parse_timezone,
    "FileAccessDate": parse_datetime_with_timezone,
    "FileInodeChangeDate": parse_datetime_with_timezone,
    "FileModifyDate": parse_datetime_with_timezone,

    "TimeCreated": parse_time_with_timezone,
    "MediaCreateDate": parse_datetime_any,
    "MediaModifyDate": parse_datetime_any,
    "CreateDate": parse_datetime_any,
    "ModifyDate": parse_datetime_any,
    "MetadataDate": parse_datetime_any,
    "ProfileDateTime": parse_datetime_any,
    "HistoryWhen": parse_datetime_any,

    "SubSecCreateDate": parse_datetime_any,
    "SubSecDateTimeOriginal": parse_datetime_any,
    "SubSecModifyDate": parse_datetime_any,

    "TrackCreateDate": parse_datetime_any,
    "TrackModifyDate": parse_datetime_any,
    "DateTimeCreated": parse_datetime_any
}


def transform_tag(tag: str, value: str) -> str:
    return TAG_MAP.get(tag, passthrough)(value)


def parse_datetime_original(data: dict[str, Any]) -> Any:
    datetime_original = data["DateTimeOriginal"]

    timezone = data.get("OffsetTimeOriginal")
    if timezone is not None:
        datetime_original = datetime_original.replace(tzinfo=timezone)

    return "DateTimeOriginal", datetime_original


def parse_datetime_digitized(data: dict[str, Any]) -> Any:
    datetime_digitized = data["DateTimeDigitized"]

    timezone = data.get("OffsetTimeDigitzed")
    if timezone is not None:
        datetime_digitized = datetime_digitized.replace(tzinfo=timezone)

    return "DateTimeDigitized", datetime_digitized


COMPOSITE_TAG_PROCESSORS = [parse_datetime_original, parse_datetime_digitized]

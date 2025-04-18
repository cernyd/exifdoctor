import datetime
from pathlib import Path

from exifdoctor.exiftool_wrapper import load_exif


EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def parse_datetime(datetime_raw: str):
    return datetime.datetime.strptime(datetime_raw, EXIF_DATETIME_FORMAT)


def format_datetime(datetime: datetime.datetime):
    return datetime.strftime(EXIF_DATETIME_FORMAT)


class ImageData:
    def __init__(self, img_path: Path):
        self.img_path: Path = img_path
        self.__exif_data = self.__load_exif_data(img_path)

    def __load_exif_data(self, img_path):
        data = load_exif(img_path)
        return data[0]

    def parse_timezone(self, tzinfo: str):
        hours, minutes = tzinfo[1:].split(":")
        offset = datetime.timedelta(hours=int(hours), minutes=int(minutes))

        if tzinfo[0] == "-":
            offset = -offset

        return datetime.timezone(offset)

    @property
    def datetime_original(self):
        datetime_original = parse_datetime(self.__exif_data["DateTimeOriginal"])

        raw_timezone = self.__exif_data.get("OffsetTimeOriginal")
        if raw_timezone is not None:
            timezone = self.parse_timezone(raw_timezone)
            datetime_original = datetime_original.replace(tzinfo=timezone)

        return datetime_original

    @property
    def datetime_digitized(self):
        datetime_digitized = parse_datetime(self.__exif_data["DateTimeDigitized"])

        raw_timezone = self.__exif_data.get("OffsetTimeDigitized")
        if raw_timezone is not None:
            timezone = self.parse_timezone(raw_timezone.decode())
            datetime_digitized = datetime_digitized.replace(tzinfo=timezone)

        return datetime_digitized

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.img_path} original={self.datetime_original.isoformat()}>"

import datetime
from pathlib import Path

import piexif


EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def parse_datetime(datetime_raw: str):
    return datetime.datetime.strptime(datetime_raw, EXIF_DATETIME_FORMAT)


def format_datetime(datetime: datetime.datetime):
    return datetime.strftime(EXIF_DATETIME_FORMAT)


class ImageData:
    def __init__(self, img_path: Path):
        self.img_path: Path = img_path
        self.__exif_data = self.__load_exif_data(img_path)

        self.__print_exif_tags()
        self.__print_gps_tags()

        # exif_bytes = piexif.dump(exif_data)
        # piexif.insert(exif_bytes, str(img.resolve()))

    def __print_exif_tags(self):
        print("Exif")
        for key, value in self.__exif_data["Exif"].items():
            print(f"\t{piexif.TAGS["Exif"][key]} = {value}")

    def __load_exif_data(self, img_path):
        with img_path.open("rb") as img_file:
            return piexif.load(img_file.read())

    def __print_gps_tags(self):
        print("GPS")
        for key, value in self.__exif_data["GPS"].items():
            print(f"\t{piexif.TAGS["GPS"][key]} = {value}")

    @property
    def __exif(self):
        return self.__exif_data["Exif"]

    def parse_timezone(self, tzinfo: str):
        hours, minutes = tzinfo[1:].split(":")
        offset = datetime.timedelta(hours=int(hours), minutes=int(minutes))

        if tzinfo[0] == "-":
            offset = -offset

        return datetime.timezone(offset)

    @property
    def datetime_original(self):
        datetime_original = parse_datetime(self.__exif.get(piexif.ExifIFD.DateTimeOriginal).decode())

        raw_timezone = self.__exif.get(piexif.ExifIFD.OffsetTimeOriginal)
        if raw_timezone is not None:
            timezone = self.parse_timezone(raw_timezone.decode())
            datetime_original = datetime_original.replace(tzinfo=timezone)

        return datetime_original

    @property
    def datetime_digitized(self):
        datetime_digitized = parse_datetime(self.__exif.get(piexif.ExifIFD.DateTimeDigitized).decode())

        raw_timezone = self.__exif.get(piexif.ExifIFD.OffsetTimeDigitized)
        if raw_timezone is not None:
            timezone = self.parse_timezone(raw_timezone.decode())
            datetime_digitized = datetime_digitized.replace(tzinfo=timezone)

        return datetime_digitized

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.img_path} original={self.datetime_original.isoformat()}>"

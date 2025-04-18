import datetime
from zoneinfo import ZoneInfo

from exifdoctor.tag_map import format_datetime


class ImageOperation:
    def apply(self, image: "ImageData"):
        ...


class TransformCreateDate(ImageOperation):
    TAGS = {"TrackCreateDate", "TrackModifyDate",
            "MediaCreateDate", "MediaModifyDate", "ModifyDate",
            "DateTimeOriginal", "CreateDate"}

    def __init__(self, offset: datetime.timedelta) -> None:
        super().__init__()
        self.offset = offset

    def apply(self, image: "ImageData"):
        for tag in self.TAGS:
            date: datetime.datetime = image.exif_data_transformed[tag]

            # Example operations
            date = date.replace(month=3, tzinfo=ZoneInfo("Europe/Prague"))
            date += self.offset
            date -= datetime.timedelta(days=1)

            image.exif_data_edits[tag].append(format_datetime(date))

        image.exif_data_edits["OffsetTimeOriginal"].append("+01:00")
        image.exif_data_edits["OffsetTimeDigitized"].append("+01:00")

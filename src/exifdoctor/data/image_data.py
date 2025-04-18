from pathlib import Path
from pprint import pprint
from typing import Any

from exifdoctor.exiftool_wrapper import load_exif
from exifdoctor.tag_map import transform_tag


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


class ImageData:
    def __init__(self, img_path: Path):
        self.img_path: Path = img_path
        self.__exif_data_input = self.__load_exif_data(img_path)
        self.__exif_data_transformed = self.transform_tags(self.__exif_data_input)
        self.__composite_tags = self.extract_composite_tags(self.__exif_data_transformed)
        pprint(self.__exif_data_transformed)

    def transform_tags(self, raw_tags: dict[str, Any]):
        tags = {}
        for key, value in raw_tags.items():
            try:
                value_transformed = transform_tag(key, value)
                tags[key] = value_transformed
            except Exception as e:
                print(f"Failed to transform tag {key}, error={e}")

        return tags

    def extract_composite_tags(self, transformed_tags: dict[str, Any]):
        tags = {}

        for processor in COMPOSITE_TAG_PROCESSORS:
            try:
                tag, value = processor(transformed_tags)
                tags[tag] = value
            except Exception:
                pass

        return tags

    def __load_exif_data(self, img_path):
        data = load_exif(img_path)
        return data[0]

from collections import defaultdict
from pathlib import Path
from typing import Any

import rich

from exifdoctor.data.image_operation import ImageOperation
from exifdoctor.exiftool_wrapper import load_exif, save_exif
from exifdoctor.tag_map import COMPOSITE_TAG_PROCESSORS, transform_tag


class ImageData:
    def __init__(self, img_path: Path):
        self.img_path: Path = img_path
        self.exif_data_raw = self.__load_exif_data(img_path)
        self.exif_data_transformed = self.transform_tags(self.exif_data_raw)
        self.exif_data_composite = self.extract_composite_tags(self.exif_data_transformed)
        self.exif_data_edits = defaultdict(list)

    def apply_image_operation(self, operation: ImageOperation):
        operation.apply(self)

    def write_changes(self):
        save_exif(self.img_path, {k: v[-1] for k, v in self.exif_data_edits.items()})

    def transform_tags(self, raw_tags: dict[str, Any]):
        tags = {}
        for key, value in raw_tags.items():
            try:
                value_transformed = transform_tag(key, value)
                tags[key] = value_transformed
            except Exception as e:
                rich.print(f"[red][ERROR]Failed to transform tag {key} with value '{value}', error={e}[/]")

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

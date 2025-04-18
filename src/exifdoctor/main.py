import datetime
import glob
from pathlib import Path

import click

from exifdoctor.data.image_data import ImageData
import rich

from exifdoctor.data.image_operation import TransformCreateDate


@click.command()
@click.option("--path", type=click.Path(exists=True))
def main(path: str):
    media_path = Path(path)
    offset = datetime.timedelta(days=1)

    for img in glob.glob(str(media_path / "**"), recursive=True):
        img = Path(img)
        try:
            if img.is_file():
                img_data = ImageData(img)
                print(img)
                img_data.apply_image_operation(TransformCreateDate(-offset))
                rich.print(f"[blue]{img_data.exif_data_transformed["Make"]} [underline]{img_data.exif_data_transformed["Model"]}[/]")
                for key, value in img_data.exif_data_transformed.items():
                    if isinstance(value, datetime.datetime):
                        rich.print(f"\t[green]{key}={value}[/]")

                for key, value in img_data.exif_data_raw.items():
                    rich.print(f"\t[yellow]{key}={value}[/]")

                rich.print(img_data.exif_data_edits)
                img_data.write_changes()

        except Exception as e:
            print(f"Failed to extract {img.resolve()} (error={e})")
            raise


if __name__ == "__main__":
    main()

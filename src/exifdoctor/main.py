import datetime
import glob
from pathlib import Path

import click

from exifdoctor.data.image_data import ImageData
import rich


@click.command()
@click.option("--path", type=click.Path(exists=True))
def main(path: str):
    media_path = Path(path)

    for img in glob.glob(str(media_path / "**"), recursive=True):
        img = Path(img)
        try:
            if img.is_file():
                img_data = ImageData(img)
                print(img)
                rich.print(img_data.exif_data_transformed)
                rich.print(f"[blue]{img_data.exif_data_transformed["Make"]} [underline]{img_data.exif_data_transformed["Model"]}[/]")
                for key, value in img_data.exif_data_transformed.items():
                    if isinstance(value, datetime.datetime):
                        rich.print(f"\t[green]{key}={value}[/]")
        except Exception as e:
            print(f"Failed to extract {img.resolve()} (error={e})")


if __name__ == "__main__":
    main()

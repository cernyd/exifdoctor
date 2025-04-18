import glob
from pathlib import Path

import click

from exifdoctor.data.image_data import ImageData


@click.command()
@click.option("--path", type=click.Path(exists=True))
def main(path: str):
    media_path = Path(path)

    for img in glob.glob(str(media_path / "**"), recursive=True):
        img = Path(img)
        try:
            if img.is_file():
                print(ImageData(img))
        except Exception as e:
            print(f"Failed to extract {img.resolve()}")


if __name__ == "__main__":
    main()

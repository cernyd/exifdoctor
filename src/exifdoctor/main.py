import glob
from pathlib import Path

from exifdoctor.data.image_data import ImageData


def main():
    image_path = Path("images")

    for img in glob.glob(str(image_path / "**"), recursive=True):
        img = Path(img)
        try:
            if img.is_file():
                print(ImageData(img))
        except Exception as e:
            print(e)
            print(f"Failed to extract {img.resolve()}")


if __name__ == "__main__":
    main()

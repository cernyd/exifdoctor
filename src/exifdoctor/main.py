from pathlib import Path

from exifdoctor.data.image_data import ImageData


def main():
    image_path = Path("images")

    for img in image_path.glob("*.JPG"):
        print(ImageData(img))


if __name__ == "__main__":
    main()

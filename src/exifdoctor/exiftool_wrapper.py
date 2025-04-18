import json
from pathlib import Path
import subprocess


def load_exif(file_path: Path):
    result = subprocess.run(
        ["exiftool", "-n", "-j", str(file_path.resolve())],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


def save_exif(file_path: Path, edits: dict[str, str]):
    command = ["exiftool"]
    for key, value in edits.items():
        command.append(f'-{key}="{value}"')

    command.append(str(file_path.resolve()))

    print(command)
    # TODO: dry run for now
    return
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

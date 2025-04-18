import json
from pathlib import Path
import subprocess


def load_exif(file_path: Path):
    result = subprocess.run(["exiftool", "-n", "-j", str(file_path.resolve())],
                            capture_output=True, text=True)
    return json.loads(result.stdout)

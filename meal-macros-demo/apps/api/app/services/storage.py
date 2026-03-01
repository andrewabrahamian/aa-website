import hashlib
from pathlib import Path
from fastapi import UploadFile

IMAGE_DIR = Path(__file__).resolve().parent.parent / "data" / "images"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def hash_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def save_image(file: UploadFile, content: bytes, image_hash: str) -> str:
    suffix = Path(file.filename or "upload.jpg").suffix or ".jpg"
    filename = f"{image_hash}{suffix}"
    path = IMAGE_DIR / filename
    if not path.exists():
        path.write_bytes(content)
    return str(path.relative_to(Path(__file__).resolve().parent.parent))

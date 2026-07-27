import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.config import settings

ALLOWED_EXTENSIONS = {'pdf', 'pptx', 'docx', 'txt'}


def ensure_upload_directory() -> Path:
    root = Path(settings.UPLOAD_DIRECTORY)
    root.mkdir(parents=True, exist_ok=True)
    return root


def validate_uploaded_file(upload_file: UploadFile) -> str:
    filename = upload_file.filename.replace(' ', '_')
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail='Unsupported file type')

    upload_file.file.seek(0, os.SEEK_END)
    file_size = upload_file.file.tell()
    upload_file.file.seek(0)
    if file_size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail='File too large')

    return ext


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    with destination.open('wb') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

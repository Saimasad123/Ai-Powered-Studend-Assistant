from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks, Form
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import DocumentRead
from app.services.document_service import create_document_record, process_document
from app.utils.file_utils import ensure_upload_directory, validate_uploaded_file, save_upload_file
from app.models.user import User
from app.models.course import Course

router = APIRouter()


def get_document_or_404(document_id: int, user_id: int, db: Session) -> Document:
    document = db.query(Document).filter(Document.id == document_id, Document.user_id == user_id).first()
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    return document


@router.post('/upload', response_model=list[DocumentRead])
def upload_documents(
    background_tasks: BackgroundTasks,
    files: list[UploadFile] = File(...),
    course_id: int | None = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if course_id is not None:
        course = db.query(Course).filter(Course.id == course_id, Course.user_id == current_user.id).first()
        if not course:
            raise HTTPException(status_code=404, detail='Course not found')

    upload_dir = ensure_upload_directory()
    saved_documents = []

    for upload_file in files:
        file_type = validate_uploaded_file(upload_file)
        safe_filename = f"{current_user.id}_{uuid4().hex}_{upload_file.filename.replace(' ', '_')}"
        destination = upload_dir / safe_filename
        save_upload_file(upload_file, destination)
        document = create_document_record(
            db=db,
            user_id=current_user.id,
            course_id=course_id,
            filename=safe_filename,
            original_filename=upload_file.filename,
            file_type=file_type,
            file_size=destination.stat().st_size,
            storage_path=str(destination),
        )
        background_tasks.add_task(process_document, document.id)
        saved_documents.append(document)
    return saved_documents


@router.get('/', response_model=list[DocumentRead])
def list_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Document).filter(Document.user_id == current_user.id).all()


@router.get('/{document_id}', response_model=DocumentRead)
def read_document(document_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_document_or_404(document_id, current_user.id, db)


@router.delete('/{document_id}')
def delete_document(document_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = get_document_or_404(document_id, current_user.id, db)
    try:
        Path(document.storage_path).unlink(missing_ok=True)
    except Exception:
        pass
    db.delete(document)
    db.commit()
    return {'detail': 'Document removed'}

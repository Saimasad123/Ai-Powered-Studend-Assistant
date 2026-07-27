import json
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.utils.document_parser import extract_document_pages, chunk_text
from app.services.llm_service import LLMService
from app.core.config import settings
from app.db.session import SessionLocal

llm_service = LLMService()


def build_chunk_metadata(document: Document, page_number: int, source_type: str) -> str:
    return json.dumps({
        'document_id': document.id,
        'document_filename': document.filename,
        'original_filename': document.original_filename,
        'page_number': page_number,
        'source_type': source_type,
    })


def process_document(document_id: int) -> None:
    db = SessionLocal()
    try:
        document = db.get(Document, document_id)
        if not document:
            return
        document.processing_status = 'processing'
        db.add(document)
        db.commit()
        db.refresh(document)

        pages = extract_document_pages(document.storage_path, document.file_type)
        if not any(page.get('text', '').strip() for page in pages):
            raise ValueError('The uploaded document contains no extractable text.')
        db.query(DocumentChunk).filter(DocumentChunk.document_id == document.id).delete(synchronize_session=False)
        chunk_index = 0
        chunks = []
        for page in pages:
            if not page['text'].strip():
                continue
            page_chunks = chunk_text(page['text'], max_tokens=400, overlap=80)
            for chunk_text_content in page_chunks:
                embedding = llm_service.create_embedding(chunk_text_content)
                metadata = build_chunk_metadata(document, page['page_number'], page['source_type'])
                chunks.append(DocumentChunk(
                    document_id=document.id,
                    course_id=document.course_id,
                    content=chunk_text_content,
                    page_number=page['page_number'],
                    chunk_index=chunk_index,
                    metadata_json=metadata,
                    embedding=embedding,
                ))
                chunk_index += 1

        if chunks:
            db.bulk_save_objects(chunks)
        document.processing_status = 'completed'
        document.processing_error = None
        db.add(document)
        db.commit()
    except Exception as exc:
        if document := db.get(Document, document_id):
            document.processing_status = 'failed'
            document.processing_error = str(exc)
            db.add(document)
            db.commit()
        raise
    finally:
        db.close()


def create_document_record(db: Session, user_id: int, course_id: int | None, filename: str, original_filename: str, file_type: str, file_size: int, storage_path: str) -> Document:
    document = Document(
        user_id=user_id,
        course_id=course_id,
        filename=filename,
        original_filename=original_filename,
        file_type=file_type,
        file_size=file_size,
        storage_path=storage_path,
        processing_status='pending',
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

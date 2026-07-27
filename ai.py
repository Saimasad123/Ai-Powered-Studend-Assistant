import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.api.dependencies import get_current_user
from app.db.session import get_db

from app.schemas.chat import (
    ChatMessageCreate,
    ChatSessionRead,
)

from app.schemas.ai import AIResponse
from app.services.rag_service import answer_question

from app.models.user import User
from app.models.chat import ChatSession
from app.models.chat_message import ChatMessage
from app.models.document_chunk import DocumentChunk
from app.models.document import Document


# =========================================================
# LOGGER
# =========================================================

logger = logging.getLogger(__name__)

router = APIRouter()


# =========================================================
# SERIALIZE CHAT SESSION
# =========================================================

def _serialize_session(session):
    messages = []

    for message in sorted(
        session.messages,
        key=lambda item: item.created_at
    ):
        citations = []

        for citation in message.citations:

            chunk = None
            document = None

            # Get SQLAlchemy database session
            db = session._sa_instance_state.session

            if db:
                chunk = db.get(
                    DocumentChunk,
                    citation.chunk_id
                )

                document = db.get(
                    Document,
                    citation.document_id
                )

            if chunk and document:
                citations.append({
                    "document_name": document.original_filename,
                    "page_number": citation.page_number,
                    "chunk_index": chunk.chunk_index,
                    "excerpt": chunk.content[:300],
                    "relevance_score": citation.relevance_score,
                })

        messages.append({
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
            "citations": citations,
        })

    return {
        "id": session.id,
        "title": session.title,
        "course_id": session.course_id,
        "course": session.course,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "messages": messages,
    }


# =========================================================
# COMMON AI EXECUTION FUNCTION
# =========================================================

def _run(request, current_user, db, mode):

    logger.info(
        "Starting AI request | mode=%s | user_id=%s | course_id=%s | session_id=%s",
        mode,
        current_user.id,
        request.course_id,
        request.session_id,
    )

    try:

        # =================================================
        # CALL RAG / AI SERVICE
        #
        # IMPORTANT:
        # answer_question() expects "prompt"
        # NOT "question"
        # =================================================

        result = answer_question(
            db=db,
            user_id=current_user.id,
            prompt=request.question,
            course_id=request.course_id,
            session_id=request.session_id,
            mode=mode,
        )

        logger.info(
            "AI request completed successfully | mode=%s | user_id=%s",
            mode,
            current_user.id,
        )

        # Convert result to AIResponse schema
        return AIResponse(**result)

    except RuntimeError as exc:

        db.rollback()

        logger.exception(
            "AI RuntimeError | mode=%s | user_id=%s",
            mode,
            current_user.id,
        )

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        db.rollback()

        logger.exception(
            "AI generation failed | mode=%s | user_id=%s",
            mode,
            current_user.id,
        )

        raise HTTPException(
            status_code=500,
            detail=f"AI generation failed: {str(exc)}",
        ) from exc


# =========================================================
# AI CHAT
# =========================================================

@router.post(
    "/chat",
    response_model=AIResponse
)
def chat(
    request: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _run(
        request,
        current_user,
        db,
        "chat",
    )


# =========================================================
# LIST CHAT SESSIONS
# =========================================================

@router.get(
    "/sessions",
    response_model=list[ChatSessionRead]
)
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    course_id: int | None = None,
):

    query = (
        db.query(ChatSession)
        .options(
            selectinload(
                ChatSession.messages
            ).selectinload(
                ChatMessage.citations
            )
        )
        .filter(
            ChatSession.user_id == current_user.id
        )
    )

    if course_id is not None:
        query = query.filter(
            ChatSession.course_id == course_id
        )

    sessions = (
        query
        .order_by(
            ChatSession.updated_at.desc()
        )
        .all()
    )

    return [
        _serialize_session(session)
        for session in sessions
    ]


# =========================================================
# READ SINGLE CHAT SESSION
# =========================================================

@router.get(
    "/sessions/{session_id}",
    response_model=ChatSessionRead
)
def read_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    session = (
        db.query(ChatSession)
        .options(
            selectinload(
                ChatSession.messages
            ).selectinload(
                ChatMessage.citations
            )
        )
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found",
        )

    return _serialize_session(session)


# =========================================================
# SUMMARIZE
# =========================================================

@router.post(
    "/summarize",
    response_model=AIResponse
)
def summarize(
    request: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _run(
        request,
        current_user,
        db,
        "summarize",
    )


# =========================================================
# GENERATE MCQs
# =========================================================

@router.post(
    "/generate-mcqs",
    response_model=AIResponse
)
def generate_mcqs(
    request: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _run(
        request,
        current_user,
        db,
        "generate-mcqs",
    )


# =========================================================
# GENERATE QUIZ
# =========================================================

@router.post(
    "/generate-quiz",
    response_model=AIResponse
)
def generate_quiz(
    request: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _run(
        request,
        current_user,
        db,
        "generate-quiz",
    )


# =========================================================
# GENERATE FLASHCARDS
# =========================================================

@router.post(
    "/generate-flashcards",
    response_model=AIResponse
)
def generate_flashcards(
    request: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _run(
        request,
        current_user,
        db,
        "generate-flashcards",
    )


# =========================================================
# EXPLAIN
# =========================================================

@router.post(
    "/explain",
    response_model=AIResponse
)
def explain(
    request: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _run(
        request,
        current_user,
        db,
        "explain",
    )


# =========================================================
# EXAM PLAN
# =========================================================

@router.post(
    "/exam-plan",
    response_model=AIResponse
)
def exam_plan(
    request: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _run(
        request,
        current_user,
        db,
        "exam-plan",
    )
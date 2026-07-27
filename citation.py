from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base


class Citation(Base):
    __tablename__ = 'citations'

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('chat_messages.id', ondelete='CASCADE'), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey('documents.id', ondelete='CASCADE'), nullable=False, index=True)
    page_number = Column(Integer, nullable=True)
    chunk_id = Column(Integer, ForeignKey('document_chunks.id', ondelete='CASCADE'), nullable=False, index=True)
    relevance_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    message = relationship('ChatMessage', back_populates='citations')

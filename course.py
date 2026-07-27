from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    course_name = Column(String(256), nullable=False)
    course_code = Column(String(64), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship('User', back_populates='courses')
    documents = relationship('Document', back_populates='course', cascade='all, delete-orphan')
    chat_sessions = relationship('ChatSession', back_populates='course', cascade='all, delete-orphan')
    quizzes = relationship('Quiz', back_populates='course', cascade='all, delete-orphan')
    flashcards = relationship('Flashcard', back_populates='course', cascade='all, delete-orphan')

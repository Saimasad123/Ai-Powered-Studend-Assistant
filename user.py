from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    courses = relationship('Course', back_populates='owner', cascade='all, delete-orphan')
    documents = relationship('Document', back_populates='owner', cascade='all, delete-orphan')
    chat_sessions = relationship('ChatSession', back_populates='user', cascade='all, delete-orphan')
    quizzes = relationship('Quiz', back_populates='user', cascade='all, delete-orphan')
    flashcards = relationship('Flashcard', back_populates='user', cascade='all, delete-orphan')

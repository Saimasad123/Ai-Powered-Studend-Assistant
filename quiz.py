from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='SET NULL'), nullable=True, index=True)
    title = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='quizzes')
    course = relationship('Course', back_populates='quizzes')
    questions = relationship('QuizQuestion', back_populates='quiz', cascade='all, delete-orphan')

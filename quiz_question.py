from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False, index=True)
    question = Column(Text, nullable=False)
    options = Column(Text, nullable=False)
    correct_answer = Column(String(256), nullable=False)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    quiz = relationship('Quiz', back_populates='questions')

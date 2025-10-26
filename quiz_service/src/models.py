from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    # questions — список объектов: [{"id": 1, "text": "...", "options": ["A","B","C"], "correct": 0}, ...]
    questions = Column(JSON, nullable=False)

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    answers = Column(JSON, nullable=False)  # {"question_id": chosen_index, ...}
    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

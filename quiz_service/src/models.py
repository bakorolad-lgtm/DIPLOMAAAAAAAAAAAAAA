from sqlalchemy import Column, ForeignKey, Integer, String, JSON, ARRAY
from src.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    questions = Column(ARRAY(JSON))


class QuizAnswers(Base):
    __tablename__ = "quiz_answers"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(ForeignKey("quizzes.id"))
    question_id = Column(Integer)
    user_id = Column(Integer)
    answer = Column(String)

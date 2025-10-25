from sqlalchemy import Column, Integer, String, Text
from src.database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    author_id = Column(Integer)

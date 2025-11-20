from sqlalchemy import Column, Integer, String, Text
from src.database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer)


class CourseBlock(Base):
    __tablename__ = "course_blocks"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer)
    text = Column(String, nullable=True)
    file_url = Column(String, nullable=True)
    elem_number = Column(Integer)

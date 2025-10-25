from pydantic import BaseModel


class QuestionSchema(BaseModel):
    id: int
    title: str
    answers: list[str]


class BaseQuizSchema(BaseModel):
    title: str
    questions: list[QuestionSchema]


class CreateQuizSchema(BaseQuizSchema):
    pass


class GetQuizSchema(BaseQuizSchema):
    id: int


class AnswerSchema(BaseModel):
    question_id: int
    answer: str


class QuizAnswerSchema(BaseModel):
    quiz_id: int
    answers: list[AnswerSchema]

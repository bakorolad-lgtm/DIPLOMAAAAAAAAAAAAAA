from pydantic import BaseModel, ConfigDict


class QuestionSchema(BaseModel):
    id: int
    title: str
    answers: list[str]
    correct_answer: str


class BaseQuizSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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

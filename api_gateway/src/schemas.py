from pydantic import BaseModel, Field, model_validator


class QuestionSchema(BaseModel):
    id: int
    title: str
    answers: list[str]
    correct_answer: str | None = None


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


class CourseBlockSchema(BaseModel):
    text: str | None = None
    file_url: str | None = None
    course_id: int | None = None
    elem_number: int | None = None

    @model_validator(mode="before")
    def check_text_or_file_url(cls, values):
        if "text" not in values and "file_url" not in values:
            raise ValueError("Either 'text' or 'file_url' must be provided.")
        if "text" in values and "file_url" in values:
            raise ValueError("Only 'text' or 'file_url' must be provided.")
        return values


class BaseCourseSchema(BaseModel):
    title: str
    blocks: list[CourseBlockSchema] = Field(default_factory=list)

class CreateCourseSchema(BaseCourseSchema):
    pass


class GetCourseSchema(BaseCourseSchema):
    id: int
    author: dict


class GetQuizCheckAnswers(BaseModel):
    title: str
    answers: list[str]
    is_correct: bool

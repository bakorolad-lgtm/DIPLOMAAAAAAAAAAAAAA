from fastapi import APIRouter, HTTPException
from src.schemas import CreateQuizSchema, QuizAnswerSchema
from src.database import async_session
from src.models import Quiz, QuizAnswers
from sqlalchemy.future import select

router = APIRouter(prefix="/quiz")

@router.get("")
async def get_quizzes():
    async with async_session() as session:
        result = await session.execute(select(Quiz))
        return result.scalars().all()

@router.post("")
async def create_quiz(quiz: CreateQuizSchema):
    async with async_session() as session:
        quiz = Quiz(
            title=quiz.title,
            questions=[question.model_dump() for question in quiz.questions]
        )
        session.add(quiz)
        await session.commit()
        return {"message": "Quiz created"}


@router.post("/answer")
async def answer_quiz(quiz_answer: QuizAnswerSchema):
    async with async_session() as session:
        quiz = await session.get(Quiz, quiz_answer.quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        for answer in quiz_answer.answers:
            print(quiz.questions)
            question_id_map = {question["id"]: question for question in quiz.questions}
            if answer.question_id not in question_id_map:
                raise HTTPException(status_code=400, detail="Invalid question id")
            if answer.answer not in question_id_map[answer.question_id]["answers"]:
                raise HTTPException(status_code=400, detail="Invalid answer")

            quiz_answer = QuizAnswers(
                quiz_id=quiz_answer.quiz_id,
                question_id=answer.question_id,
                answer=answer.answer
            )
            session.add(quiz_answer)
        await session.commit()
        return {"message": "Quiz answered"}

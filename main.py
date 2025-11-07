# import asyncio
# from sqlalchemy import distinct, select
# from quiz_service.src.database import async_session
# from quiz_service.src.models import Quiz, QuizAnswers

# async def main():
#     user_id = 2
#     async with async_session() as session:
#         filtered_quizes = (await session.execute(
#             select(distinct(Quiz.id), Quiz.title)
#             .join(QuizAnswers, Quiz.id == QuizAnswers.quiz_id)
#             .where(
#                 QuizAnswers.user_id == user_id
#             )
#         )).scalars()
#         print(list(filtered_quizes))

# if __name__ == "__main__":
#     asyncio.run(main())





from user_service.src.utils import verify_password


bd_pass = "$2b$12$HGRLLbvmhy1jPc3S8JxPUeg56gD4d7IVD.XIsY5m8mTQobcNF5YeO"

print(verify_password("1234567890", bd_pass))
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from Models.UserAnswers import UserAnswers
from Services.user_service import find_question_check_answer

userrouter = APIRouter(tags=['User answers'])


@userrouter.post('/answer')
async def create_question_with_answers(useranswer: UserAnswers):
    answer = jsonable_encoder(useranswer)
    await find_question_check_answer(answer)

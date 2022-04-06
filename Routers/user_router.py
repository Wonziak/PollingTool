from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from Models.UserAnswers import UserAnswers
from Services.user_service import find_question_check_answer

userrouter = APIRouter(tags=['User answers'])


@userrouter.post('/answer')
async def send_user_answer(useranswer: UserAnswers):
    answer = jsonable_encoder(useranswer)
    await find_question_check_answer(answer)

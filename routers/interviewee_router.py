from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from models.interviewee_answers import IntervieweeAnswers
from services.interviewee_service import find_question_check_answer

interviewee_router = APIRouter(tags=['User answers'])


@interviewee_router.post('/answer')
async def send_user_answer(intervieweeanswers: IntervieweeAnswers):
    answer = jsonable_encoder(intervieweeanswers)
    await find_question_check_answer(answer)
"""
This file contains answer to questions routes:
    - post('/answer')
"""
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from models.interviewee_answers import IntervieweeAnswers
from services.interviewee_service import find_question_check_answer

interviewee_router = APIRouter(tags=['User answers'])


@interviewee_router.post('/answer')
async def send_user_answer(interviewee_answers: IntervieweeAnswers):
    """
    This endpoint allows user to send answer to poll.
    :param interviewee_answers: {
                "question_id": '624c4d993922d0c5d2c54108',
                "answer": 'B'
            }
    :return: HTTP exception with code 200 and message "Congratulation! Your answer is correct!"
    if answer was correct. HTTP exception with code 200 and message
    "Your answer is incorrect! Please try again." if answer was incorrect. HTTP exception with code
    400 and message "Invalid question id" if question id was invalid. HTTP exception with code
    404 and message "Could not find question" if question not found.
    """
    answer = jsonable_encoder(interviewee_answers)
    await find_question_check_answer(answer)

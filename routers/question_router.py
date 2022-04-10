"""
This file contains feedback form routes:
    - post('/question'),
    - get('/question/{question_id}'),
    - get('/question'),
    - put('/question/{question_id}'),
    - delete('/question/{question_id}').
"""
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.question_answers import QuestionAnswers, response_model, UpdateQuestionAnswers
from services.question_service import add_questionanswer, retrieve_questionanswer, \
    retrieve_all_questionanswer, \
    update_questionanswer, delete_questionanswers

question_router = APIRouter(tags=['Question'])


@question_router.post('/question')
async def create_question_with_answers(question: QuestionAnswers):
    """
    This endpoint allows user to create question with answers and set correct answer.
    :param question: {
                "question": "What kind of bear is best?",
                "answers": {'A': "That's a ridiculous question.",
                            'B': "Black bear"},
                "correctAnswer": 'B'
            }
    :return: dictionary containing created question,"Question with answers added successfully."
    message with HTTP code 200, or raises HTTP exception with code 400
    if question could not be created.
    """
    question = jsonable_encoder(question)
    new_question = await add_questionanswer(question)
    return response_model(new_question, "Question with answers added successfully.")


@question_router.get('/question/{question_id}')
async def get_question_by_id(question_id: str):
    """
    This endpoint allows user to get question with answers, stored in database, by id.
    :param question_id:  id of question.
    :return: dictionary containing question, without correct answer field, retrieved by id,
    "Question with id: {question_id} retrieved." message with HTTP code 200. Raises HTTP exception
    with code 404 if question not found or 400 if id is invalid.
    """
    question = await retrieve_questionanswer(question_id)
    return response_model(question, f'Question with id: {question_id} retrieved.'.format(
        question_id=question_id))


@question_router.get('/question')
async def get_all_questions():
    """
    This endpoint allows user to retrieved all submitted questions with answers.
    :return: dictionary containing all questions with answers from database without showing
    correct answers, "All questions listed" message with code 200
    or raises HTTP 404 exception if none question found.
        """
    questions = await retrieve_all_questionanswer()
    return response_model(questions, "All questions listed.")


@question_router.put('/question/{question_id}')
async def update_question_by_id(question: UpdateQuestionAnswers, question_id: str):
    """
        This endpoint allows user to update submitted question with answers.
        :param question: {
                optional: "question": "What kind of bear is best?",
                optional: "answers": {'A': "That's a ridiculous question.",
                            'B': "Black bear"},
                optional: "correctAnswer": 'B'
            }
        :param question_id: id of question.
        :return: dictionary containing question retrieved by id,
        "Question with id: {question_id} updated." message with HTTP code 200. Raises HTTP exception
        with code 404 if question not found or 400 if id is invalid.
        """
    question = jsonable_encoder(question)
    questions = await update_questionanswer(question_id, question)
    return response_model(questions, f'Question with id: {question_id} updated.'.format(
        question_id=question_id))


@question_router.delete('/question/{question_id}')
async def delete_question_by_id(question_id: str):
    """
    This endpoint allows user to delete submitted question.
    :param question_id: id of question.
    :return: dictionary containing "Question with id: {question_id} deleted." message
    with HTTP code 200. Raises HTTP exception with code 404 if question not found
    or 400 if id is invalid.
    """
    result = await delete_questionanswers(question_id)
    if result:
        return response_model(
            f'Question with id: {question_id} retrieved.'.format(question_id=question_id))

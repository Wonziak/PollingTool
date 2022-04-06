from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from Models.QuestionAnswers import QuestionAnswers, response_model,UpdateQuestionAnswers
from Services.questionanswer_service import add_questionanswer, retrieve_questionanswer, retrieve_all_questionanswers, \
    update_questionanswer, delete_questionanswers

questionrouter = APIRouter(tags=['Question'])


@questionrouter.post('/question')
async def create_question_with_answers(question: QuestionAnswers):
    question = jsonable_encoder(question)
    new_question = await add_questionanswer(question)
    return response_model(new_question, "Question with answers added successfully.")


@questionrouter.get('/question/{question_id}')
async def get_question_by_id(question_id: str):
    question = await retrieve_questionanswer(question_id)
    return response_model(question, f'Question with id: {question_id} retrieved.'.format(question_id=question_id))


@questionrouter.get('/questions')
async def get_all_questions():
    questions = await retrieve_all_questionanswers()
    return response_model(questions, "All questions listed.")


@questionrouter.put('/question/{question_id}')
async def update_question(question: UpdateQuestionAnswers, question_id: str):
    question = jsonable_encoder(question)
    questions = await update_questionanswer(question_id, question)
    return response_model(questions, f'Question with id: {question_id} updated.'.format(question_id=question_id))


@questionrouter.delete('/question/{question_id}')
async def delete_question_by_id(question_id: str):
    result = await delete_questionanswers(question_id)
    if result:
        return response_model(f'Question with id: {question_id} retrieved.'.format(question_id=question_id))

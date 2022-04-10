"""
This file contains service functions for questionanswer:
    - add_questionanswer,
    - retrieve_all_questionanswers,
    - retrieve_questionanswer,
    - update_questionanswer,
    - delete_questionanswer,
    - questionanswer_helper_post,
    - questionanswer_helper_get.
"""
from bson.objectid import ObjectId
from fastapi import HTTPException
from database.database import question_answer_collection


async def add_questionanswer(questionanswer_data: dict) -> dict:
    """
    This function creates new question with answers in database, returns it as a dictionary
    or raises HTTP exception with code 404 and message "Could not create question"
    if could not create question.
    :param questionanswer_data:
    {
        "question": "What kind of bear is best?",
        "answers": {'A': "That's a ridiculous question.",
                    'B': "Black bear"},
        "correctAnswer": 'B'
    }
    :return: newly created question with answers as a dictionary:
    {
        "id": id,
        "question": question,
        "answers": {answers},
        "correctAnswer": correctAnswer
    }
    """
    if not questionanswer_data['correctAnswer'] in questionanswer_data['answers'].keys():
        raise HTTPException(status_code=400, detail="Could not create question")
    question_answers = question_answer_collection.insert_one(questionanswer_data)
    new_question_answers = question_answer_collection.find_one(
        {'_id': question_answers.inserted_id})
    return questionanswer_helper_post(new_question_answers)


async def retrieve_all_questionanswer():
    """
    This function searches for all questions with answers in database, stores them in array
    as a dictionaries and returns this array. Question dictionaries do not contain 'correctAnswer'
    field.
    If none feedback found raises HTTP exception with code 404
    and message "Could not find any question".
    :return: Array of dictionaries:
    [{
        "id": id,
        "question": question,
        "answers": {answers}
    }]
    """
    question_answers = []
    for entry in question_answer_collection.find():
        question_answers.append(questionanswer_helper_get(entry))
    if len(question_answers) == 0:
        raise HTTPException(status_code=404, detail="Could not find any question")
    return question_answers


async def retrieve_questionanswer(question_id: str) -> dict:
    """
    This function searches for question with answers in database by id
    and returns it as a dictionary without 'correctAnswer' field.
    If question with answers not found raises HTTP exception with code 404 and message
    "Could not find question with id: {question_id}". If question id is invalid raises
    HTTP exception with code 400 and message "Invalid question id".
    :param question_id: id of question.
    :return: question as a dictionary:
    {
        "id": id,
        "question": question,
        "answers": {answers}
    }
    """
    if len(question_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid question id")
    question_answers = question_answer_collection.find_one({'_id': ObjectId(question_id)})
    if question_answers:
        return questionanswer_helper_get(question_answers)
    raise HTTPException(status_code=404,
                        detail=f'Could not find question with id: {question_id}.'.format(
                            question_id=question_id))


async def update_questionanswer(question_id: str, data: dict):
    """
    This function searches for question with answers in database by id,
    updates its fields and raises HTTP exception with code 200 if question with answers updated.
    If question not found raises HTTP exception with code 404 and message
    "Could not find question with id: {question_id}".
    If could not update question raises HTTP exception with code 409 and message
    "Could not update question with id: {question_id}". If question id is invalid raises
    HTTP exception with code 400 and message "Invalid question id".
    :param question_id: id of question
    :param data: question with answers as a dictionary:
    {
        optional: "question": question,
        optional: "answers": {answers},
        optional: "correctAnswer": correctAnswer
    }
    :return: updated question as dictionary:
    {
        "id": id,
        "question": question,
        "answers": {answers},
        "correctAnswer": correctAnswer
    }
    """
    if len(question_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid question id")
    question_answers = question_answer_collection.find_one({"_id": ObjectId(question_id)})
    if question_answers:
        for key in question_answers.keys():
            if key in data.keys() and data[key] is None:
                data[key] = question_answers[key]
        updated_question_answers = question_answer_collection.update_one(
            {"_id": ObjectId(question_id)}, {"$set": data}
        )
        if updated_question_answers:
            raise HTTPException(status_code=200,
                                detail=f'Question with id: {question_id} updated.'.format(
                                    question_id=question_id))
        raise HTTPException(status_code=409,
                            detail=f'Could not update question with id: {question_id}.'.format(
                                question_id=question_id))
    raise HTTPException(status_code=404,
                        detail=f'Could not find question with id: {question_id}.'.format(
                            question_id=question_id))


async def delete_questionanswers(question_id: str):
    """
    This function searches for question with answer in database by id and deletes it.
    If question found and deleted raises HTTP exception with code 200 and message
    "Question with id: {question_id} deleted.". If question not found raises HTTP exception
    with code 404 and message "Could not find question with id: {question_id}".
    If question id is invalid raises HTTP exception with code 400 and message "Invalid question id".
    :param question_id: id of question.
    :return: HTTP status code and message.
    """
    if len(question_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid question id")
    student = question_answer_collection.find_one({"_id": ObjectId(question_id)})
    if student:
        question_answer_collection.delete_one({"_id": ObjectId(question_id)})
        raise HTTPException(status_code=200,
                            detail=f'Question with id: {question_id} deleted.'.format(
                                question_id=question_id))
    raise HTTPException(status_code=404,
                        detail=f'Could not find question with id: {question_id}.'.format(
                            question_id=question_id))


def questionanswer_helper_post(questionanswer) -> dict:
    """
    This function converts MongoDB questionanswer object into dictionary and returns it.
    Dictionary returned by this function contains 'correctAnswer' field so user can see if it is
    correct after posting question.
    :param questionanswer: MongoDB questionanswer object.
    :return: {
        "id": questionanswer_id,
        "question": questionanswer_question,
        "answers": questionanswer_answers,
        "correctAnswer": questionanswer_correctAnswer
    }
    """
    return {
        "id": str(questionanswer['_id']),
        "question": questionanswer['question'],
        "answers": str(questionanswer['answers']),
        "correctAnswer": questionanswer['correctAnswer']
    }


def questionanswer_helper_get(questionanswer) -> dict:
    """
    This function converts MongoDB questionanswer object into dictionary and returns it.
    Dictionary returned by this function does not contain 'correctAnswer' field so user who wants
    to answer question can not see correct answer.
    :param questionanswer: MongoDB questionanswer object.
    :return: {
        "id": questionanswer_id,
        "question": questionanswer_question,
        "answers": questionanswer_answers,
        "correctAnswer": questionanswer_correctAnswer
    }
    """
    return {
        "id": str(questionanswer['_id']),
        "question": questionanswer['question'],
        "answers": str(questionanswer['answers'])
    }

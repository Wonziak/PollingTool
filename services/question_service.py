from bson.objectid import ObjectId
from fastapi import HTTPException
from database.database import question_answer_collection


async def add_questionanswer(questionanswers_data: dict) -> dict:
    if not questionanswers_data['correctAnswer'] in questionanswers_data['answers'].keys():
        raise HTTPException(status_code=400, detail="Could not create question")
    question_answers = question_answer_collection.insert_one(questionanswers_data)
    new_question_answers = question_answer_collection.find_one({'_id': question_answers.inserted_id})
    return questionanswer_helper_post(new_question_answers)


async def retrieve_all_questionanswers():
    question_answers = []
    for entry in question_answer_collection.find():
        question_answers.append(questionanswer_helper_get(entry))
    if len(question_answers) == 0:
        raise HTTPException(status_code=404, detail="Could not find any question")
    return question_answers


async def retrieve_questionanswer(question_id: str) -> dict:
    if len(question_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid question id")
    question_answers = question_answer_collection.find_one({'_id': ObjectId(question_id)})
    if question_answers:
        return questionanswer_helper_get(question_answers)
    else:
        raise HTTPException(status_code=404, detail=f'Could not find question with id: {question_id}.'.format(
            question_id=question_id))


async def update_questionanswer(question_id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(question_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid question id")
    question_answers = question_answer_collection.find_one({"_id": ObjectId(question_id)})
    if question_answers:
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
    return {
        "id": str(questionanswer['_id']),
        "question": questionanswer['question'],
        "answers": str(questionanswer['answers']),
        "correctAnswer": questionanswer['correctAnswer']
    }


def questionanswer_helper_get(questionanswer) -> dict:
    return {
        "id": str(questionanswer['_id']),
        "question": questionanswer['question'],
        "answers": str(questionanswer['answers'])
    }

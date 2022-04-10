"""
This file contains service functions for interviewee answer:
    - find_question_check_answer.
"""
from bson.objectid import ObjectId
from fastapi import HTTPException
from database.database import question_answer_collection


async def find_question_check_answer(intervieweeanswers: dict):
    """
    This function checks if interviewee answer for question is correct. If answer is correct
    it raises HTTP exception with code 200 and massage "Congratulation! Your answer is correct!".
    If answer is incorrect raises HTTP exception with code 200 and massage
    "Your answer is incorrect! Please try again.". If question id is invalid it raises
    HTTP exception with code 400 and message "Invalid question id". If question not found in
    database it raises HTTP exception with code 404 and message "Could not find question".
    :param intervieweeanswers:{
        "question_id": '624c4d993922d0c5d2c54108',
        "answer": 'B'
    }
    :return: HTTP exception with status code and message.
    """
    question_id = intervieweeanswers['question_id']
    if len(question_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid question id")
    question_answers = question_answer_collection.find_one({'_id': ObjectId(question_id)})
    if question_answers:
        if question_answers['correctAnswer'] == intervieweeanswers['answer']:
            raise HTTPException(status_code=200, detail="Congratulation! Your answer is correct!")
        raise HTTPException(status_code=200,
                            detail="Your answer is incorrect! Please try again.")
    raise HTTPException(status_code=404, detail="Could not find question")

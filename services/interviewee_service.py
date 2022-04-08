from bson.objectid import ObjectId
from fastapi import HTTPException
from database.database import question_answer_collection


async def find_question_check_answer(intervieweeanswers: dict):
    question_id = intervieweeanswers['question_id']
    if len(question_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid question id")
    question_answers = question_answer_collection.find_one({'_id': ObjectId(question_id)})
    if question_answers:
        if question_answers['correctAnswer'] == intervieweeanswers['answer']:
            raise HTTPException(status_code=200, detail="Congratulation! Your answer is correct!")
        else:
            raise HTTPException(status_code=200, detail="Your answer is incorrect! Please try again.")
    else:
        raise HTTPException(status_code=404, detail="Could not find question")

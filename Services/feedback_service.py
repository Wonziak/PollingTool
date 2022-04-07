from bson.objectid import ObjectId
from fastapi import HTTPException
from Database.database import feedback_collection


async def add_feedback(feedback_form: dict) -> dict:
    feedback = feedback_collection.insert_one(feedback_form)
    new_feedback = feedback_collection.find_one({'_id': feedback.inserted_id})
    return feedback_helper(new_feedback)


async def retrieve_all_feedbacks():
    feedbacks = []
    for entry in feedback_collection.find():
        feedbacks.append(feedback_helper(entry))
    if len(feedbacks) == 0:
        raise HTTPException(status_code=404, detail="Could not find any feedback")
    return feedbacks


async def retrieve_feedback(feedback_id: str) -> dict:
    if len(feedback_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid feedback id")
    feedback = feedback_collection.find_one({'_id': ObjectId(feedback_id)})
    if feedback:
        return feedback_helper(feedback)
    else:
        raise HTTPException(status_code=404, detail=f'Could not find feedback with id: {feedback_id}.'.format(
            feedback_id=feedback_id))


async def update_feedback(feedback_id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(feedback_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid feedback id")
    question_answers = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
    if question_answers:
        updated_question_answers = feedback_collection.update_one(
            {"_id": ObjectId(feedback_id)}, {"$set": data}
        )
        if updated_question_answers:
            raise HTTPException(status_code=200,
                                detail=f'Feedback with id: {feedback_id} updated.'.format(
                                    feedback_id=feedback_id))
        raise HTTPException(status_code=409,
                            detail=f'Could not update feedback with id: {feedback_id}.'.format(
                                feedback_id=feedback_id))
    raise HTTPException(status_code=404,
                        detail=f'Could not find feedback with id: {feedback_id}.'.format(
                            feedback_id=feedback_id))


async def delete_feedback(feedback_id: str):
    if len(feedback_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid feedback id")
    student = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
    if student:
        feedback_collection.delete_one({"_id": ObjectId(feedback_id)})
        raise HTTPException(status_code=200,
                            detail=f'Feedback with id: {feedback_id} deleted.'.format(
                                feedback_id=feedback_id))
    raise HTTPException(status_code=404,
                        detail=f'Could not find feedback with id: {feedback_id}.'.format(
                            feedback_id=feedback_id))


def feedback_helper(feedback) -> dict:
    return {
        "id": str(feedback['_id']),
        "title": str(feedback['title']),
        "summary": str(feedback['summary'])
    }

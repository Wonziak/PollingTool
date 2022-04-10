"""
This file contains service functions for feedback form:
    - add_feedback,
    - retrieve_all_feedbacks,
    - retrieve_feedback,
    - update_feedback,
    - delete_feedback,
    - feedback_helper.
"""
from bson.objectid import ObjectId
from fastapi import HTTPException
from database.database import feedback_collection


async def add_feedback(feedback_form: dict) -> dict:
    """
    This function creates new feedback in database, returns it as a dictionary
    or raises HTTP exception with code 404 and message "Could not create feedback"
    if could not create form.
    :param feedback_form: {
        "title": "Title of feedback",
        "summary": "This is excellent!"
    }
    :return: newly created feedback as a dictionary:
        {
        "id": id,
        "title": title,
        "summary": summary
        }
    """
    feedback = feedback_collection.insert_one(feedback_form)
    new_feedback = feedback_collection.find_one({'_id': feedback.inserted_id})
    if not new_feedback:
        raise HTTPException(status_code=400, detail="Could not create feedback")
    return feedback_helper(new_feedback)


async def retrieve_all_feedbacks():
    """
    This function searches for all feedbacks in database, stores them in array as a dictionaries
    and returns this array. If none feedback found raises HTTP exception with code 404
    and message "Could not find any feedback".
    :return: Array of dictionaries:
    [{
        "id": id,
        "title": title,
        "summary": summary
    }]
    """
    feedbacks = []
    for entry in feedback_collection.find():
        feedbacks.append(feedback_helper(entry))
    if len(feedbacks) == 0:
        raise HTTPException(status_code=404, detail="Could not find any feedback")
    return feedbacks


async def retrieve_feedback(feedback_id: str) -> dict:
    """
    This function searches for feedback in database by id and returns it as a dictionary.
    If feedback not found raises HTTP exception with code 404 and message
    "Could not find feedback with id: {feedback_id}". If feedback id is invalid raises
    HTTP exception with code 400 and message "Invalid feedback id".
    :param feedback_id: id of feedback.
    :return: feedback as a dictionary:
     {
        "id": id,
        "title": title,
        "summary": summary
    }
    """
    if len(feedback_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid feedback id")
    feedback = feedback_collection.find_one({'_id': ObjectId(feedback_id)})
    if feedback:
        return feedback_helper(feedback)
    raise HTTPException(status_code=404,
                        detail=f'Could not find feedback with id: {feedback_id}.'.format(
                            feedback_id=feedback_id))


async def update_feedback(feedback_id: str, data: dict):
    """
    This function searches for feedback in database by id, updates its fields and raises
    HTTP exception with code 200 if feedback updated. If feedback not found raises
    HTTP exception with code 404 and message "Could not find feedback with id: {feedback_id}".
    If could not update feedback raises HTTP exception with code 409 and message
    "Could not update feedback with id: {feedback_id}". If feedback id is invalid raises
    HTTP exception with code 400 and message "Invalid feedback id".
    :param feedback_id: id of feedback
    :param data: feedback as a dictionary:
    {
        optional: "title": "Title of feedback",
        optional: "summary": "This is excellent!"
    }
    :return: updated feedback as dictionary:
    {
        "id": id,
        "title": title,
        "summary": summary
    }
    """
    if len(feedback_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid feedback id")
    feedback = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
    if feedback:
        for key in feedback.keys():
            if key in data.keys() and data[key] is None:
                data[key] = feedback[key]
        updated_feedback = feedback_collection.update_one(
            {"_id": ObjectId(feedback_id)}, {"$set": data}
        )
        if updated_feedback:
            feedback = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
            return feedback_helper(feedback)
        raise HTTPException(status_code=409,
                            detail=f'Could not update feedback with id: {feedback_id}.'.format(
                                feedback_id=feedback_id))
    raise HTTPException(status_code=404,
                        detail=f'Could not find feedback with id: {feedback_id}.'.format(
                            feedback_id=feedback_id))


async def delete_feedback(feedback_id: str):
    """
    This function searches for feedback in database by id and deletes it.
    If feedback found and deleted raises HTTP exception with code 200 and message
    "Feedback with id: {feedback_id} deleted.". If feedback not found raises HTTP exception
    with code 404 and message "Could not find feedback with id: {feedback_id}".
    If feedback id is invalid raises HTTP exception with code 400 and message "Invalid feedback id".
    :param feedback_id: id of feedback.
    :return: HTTP status code and message.
    """
    if len(feedback_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid feedback id")
    feedback = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
    if feedback:
        feedback_collection.delete_one({"_id": ObjectId(feedback_id)})
        raise HTTPException(status_code=200,
                            detail=f'Feedback with id: {feedback_id} deleted.'.format(
                                feedback_id=feedback_id))
    raise HTTPException(status_code=404,
                        detail=f'Could not find feedback with id: {feedback_id}.'.format(
                            feedback_id=feedback_id))


def feedback_helper(feedback) -> dict:
    """
    This function converts MongoDB feedback object into dictionary and returns it.
    :param feedback: MongoDB feedback object.
    :return: {
        "id": feedback_id,
        "title": feedback_title,
        "summary": feedback_summary
    }
    """
    return {
        "id": str(feedback['_id']),
        "title": str(feedback['title']),
        "summary": str(feedback['summary'])
    }

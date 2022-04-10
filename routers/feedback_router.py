"""
This file contains feedback form routes:
    - post('/feedback'),
    - get('/feedback/{feedback_id}'),
    - get('/feedback'),
    - put('/feedback/{feedback_id}'),
    - delete('/feedback/{feedback_id}').
"""
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models.feedback_form import FeedbackForm, UpdateFeedbackForm, response_model
from services.feedback_service import add_feedback, retrieve_feedback, retrieve_all_feedbacks, \
    update_feedback, delete_feedback

feedback_router = APIRouter(tags=["Feedback"])


@feedback_router.post('/feedback')
async def create_feedback(feedback_form: FeedbackForm):
    """
    This endpoint allows user to create and submit feedback.
    :param feedback_form:  {
        "title": "Title of feedback",
        "summary": "This is excellent!"
    }
    :return: dictionary containing created form,"Feedback submitted successfully. Thank you!"
    message with HTTP code 201, or raises HTTP exception with code 400 if feedback could
    not be created.
    """
    feedback_form = jsonable_encoder(feedback_form)
    new_feedback = await add_feedback(feedback_form)
    return response_model(new_feedback, "Feedback submitted successfully. Thank you!", code=201)


@feedback_router.get('/feedback/{feedback_id}')
async def get_feedback_by_id(feedback_id: str):
    """
    This endpoint allows user to get one feedback, stored in database, by id.
    :param feedback_id:  id of feedback.
    :return: dictionary containing form retrieved by id,
    "Feedback with id: {feedback_id} retrieved." message with HTTP code 200. Raises HTTP exception
    with code 404 if feedback not found or 400 if id is invalid.
    """
    feedback = await retrieve_feedback(feedback_id)
    return response_model(feedback, f'Feedback with id: {feedback_id} retrieved.'.format(
        feedback_id=feedback_id))


@feedback_router.get('/feedback')
async def get_all_feedbacks():
    """
    This endpoint allows user to retrieved all submitted feedbacks.
    :return: dictionary containing all feedbacks from database, "All feedbacks listed." message
    with code 200 or raises HTTP 404 exception if none feedback found.
    """
    feedbacks = await retrieve_all_feedbacks()
    return response_model(feedbacks, "All feedbacks listed.")


@feedback_router.put('/feedback/{feedback_id}')
async def update_feedback_by_id(feedback_form: UpdateFeedbackForm, feedback_id: str):
    """
    This endpoint allows user to update submitted feedback.
    :param feedback_form:{
        optional: "title": "Title of feedback",
        optional: "summary": "This is excellent!"
    }
    :param feedback_id: id of feedback.
    :return: dictionary containing updated feedback as dictionary,
    "Feedback with id: {feedback_id} updated." message with HTTP code 200. Raises HTTP exception
    with code 404 if feedback not found or 400 if id is invalid.
    """
    feedback_form = jsonable_encoder(feedback_form)
    updated_feedback_form = await update_feedback(feedback_id, feedback_form)
    return response_model(updated_feedback_form,
                          f'Feedback with id: {feedback_id} updated.'.format(
                              feedback_id=feedback_id))


@feedback_router.delete('/feedback/{feedback_id}')
async def delete_feedback_by_id(feedback_id: str):
    """
    This endpoint allows user to delete submitted feedback.
    :param feedback_id: id of feedback.
    :return: dictionary containing "Feedback with id: {feedback_id} deleted." message
    with HTTP code 200. Raises HTTP exception with code 404 if feedback not found
    or 400 if id is invalid.
    """
    result = await delete_feedback(feedback_id)
    if result:
        return response_model(
            f'Feedback with id: {feedback_id} deleted.'.format(feedback_id=feedback_id))

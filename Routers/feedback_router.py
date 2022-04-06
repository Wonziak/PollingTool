from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from Models.FeedbackForm import FeedbackForm, UpdateFeedbackForm, response_model
from Services.feedback_service import add_feedback, retrieve_feedback, retrieve_all_feedbacks, \
    update_feedback, delete_feedback

feedback_router = APIRouter(tags=["Feedback"])


@feedback_router.post('/feedback')
async def create_feedback(feedbackForm: FeedbackForm):
    feedbackForm = jsonable_encoder(feedbackForm)
    new_feedback = await add_feedback(feedbackForm)
    return response_model(new_feedback, "Feedback submitted successfully")


@feedback_router.get('/feedback/{feedback_id}')
async def get_feedback_by_id(feedback_id: str):
    feedback = await retrieve_feedback(feedback_id)
    return response_model(feedback, f'Feedback with id: {feedback_id} retrieved.'.format(feedback_id=feedback_id))


@feedback_router.get('/feedback')
async def get_all_feedbacks():
    feedbacks = await retrieve_all_feedbacks()
    return response_model(feedbacks, "All feedbacks listed.")


@feedback_router.put('/feedback/{feedback_id}')
async def update_feedback_by_id(feedbackForm: FeedbackForm, feedback_id: str):
    feedbackForm = jsonable_encoder(feedbackForm)
    updated_feedbackForm = await update_feedback(feedback_id, feedbackForm)
    return response_model(updated_feedbackForm,
                          f'Question with id: {feedback_id} updated.'.format(feedback_id=feedback_id))


@feedback_router.delete('/feedback/{feedback_id}')
async def delete_feedback_by_id(feedback_id: str):
    result = await delete_feedback(feedback_id)
    if result:
        return response_model(f'Feedback with id: {feedback_id} retrieved.'.format(feedback_id=feedback_id))

import pytest

from Services.feedback_service import add_feedback, retrieve_all_feedbacks

feedbackForm = {
    "title": "test form",
    "summary": "summary of test form",
}


@pytest.mark.asyncio
async def test_should_creat_new_form():
    response = await add_feedback(feedbackForm)
    assert response["title"] == "test form"


@pytest.mark.asyncio
async def test_should_return_list_of_feedbacks():
    response = await retrieve_all_feedbacks()
    assert len(response) > 0

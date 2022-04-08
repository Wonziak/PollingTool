import pytest

from services.question_service import add_questionanswer, retrieve_all_questionanswers

questionanswer = {
    "question": "What kind of bear is best?",
    "answers": {'A': "That's a ridiculous question.",
                'B': "Black bear"},

    "correctAnswer": 'B'
}


@pytest.mark.asyncio
async def test_should_creat_new_questionanswers():
    response = await add_questionanswer(questionanswer)
    assert response["correctAnswer"] == "B"


@pytest.mark.asyncio
async def test_should_return_list_of_questionanswers():
    response = await retrieve_all_questionanswers()
    assert len(response) > 0

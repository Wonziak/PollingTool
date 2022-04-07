import pytest
from fastapi.testclient import TestClient

from main import app

questionanswer = {
    "question": "What kind of bear is best?",
    "answers": {'A': "That's a ridiculous question.",
                'B': "Black bear"},

    "correctAnswer": 'B'
}

client = TestClient(app)


@pytest.mark.asyncio
async def test_should_create_questionanswer():
    response = client.post("/question", json=questionanswer)
    assert response.status_code == 200
    assert response.json()['data'][0]['question'] == 'What kind of bear is best?'


@pytest.mark.asyncio
async def test_should_return_all_questionaswers():
    response = client.get("/question")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_should_return_http_code_400_and_invalid_question_id():
    response = client.get("/question/123")
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid question id'


@pytest.mark.asyncio
async def test_should_not_find_question_by_id():
    question_id = "624ed6ac8a361b879616f878"
    response = client.get(f"/question/{question_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == f"Could not find question with id: {question_id}."

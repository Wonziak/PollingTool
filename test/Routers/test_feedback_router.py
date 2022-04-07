import pytest
from fastapi.testclient import TestClient

from main import app

feedbackForm = {
    "title": "test form",
    "summary": "summary of test form",
}

client = TestClient(app)


@pytest.mark.asyncio
async def test_should_create_feedback():
    response = client.post("/feedback", json=feedbackForm)
    assert response.status_code == 200
    assert response.json()['data'][0]['title'] == 'test form'


@pytest.mark.asyncio
async def test_should_return_all_feedbacks():
    response = client.get("/feedback")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_should_return_http_code_400_and_invalid_question_id():
    response = client.get("/feedback/123")
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid feedback id'


@pytest.mark.asyncio
async def test_should_not_find_question_by_id():
    question_id = "624ed6ac8a361b879616f828"
    response = client.get(f"/feedback/{question_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == f"Could not find feedback with id: {question_id}."

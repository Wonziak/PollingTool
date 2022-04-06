from pydantic import BaseModel
from typing import Optional, Dict
from uuid import uuid1


class QuestionAnswers(BaseModel):
    question: str
    answers: Dict[str, str]
    correctAnswer: str

    class Config:
        schema_extra = {
            "example": {
                "question": "What kind of bear is best?",
                "answers": {'A': "That's a ridiculous question.",
                            'B': "Black bear"},

                "correctAnswer": 'B'
            }
        }


class UpdateQuestionAnswers(BaseModel):
    question: Optional[str]
    answers: Optional[Dict[str, str]]
    correctAnswer: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "Question": "What kind of bear is best?",
                "answers": {'A': "That's a ridiculous question.",
                            'B': "Black bear"},
                "correctAnswer": 'B'
            }
        }


def response_model(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional, Dict


class QuestionAnswers(BaseModel):
    question: str = Field(min_length=1, max_length=100)
    answers: Dict[str, str]
    correctAnswer: str = Field(min_length=1, max_length=1)

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

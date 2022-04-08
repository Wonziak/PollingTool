"""
This file contains:
    QuestionAnswers class,
    UpdateQuestionAnswers class,
    and response_model function.
"""
from typing import Optional, Dict
from pydantic import BaseModel
from pydantic.fields import Field


class QuestionAnswers(BaseModel):
    """
    This class is model for interviewee answer. It contains fields 'question' and 'answers'
    and 'correctAnswer', which are required.
    """
    question: str = Field(min_length=1, max_length=100)
    answers: Dict[str, str]
    correctAnswer: str = Field(min_length=1, max_length=1)

    class Config:
        """
        This class shows how should request look like.
        """
        schema_extra = {
            "example": {
                "question": "What kind of bear is best?",
                "answers": {'A': "That's a ridiculous question.",
                            'B': "Black bear"},

                "correctAnswer": 'B'
            }
        }


class UpdateQuestionAnswers(BaseModel):
    """
    This class is model for updating interviewee answer. It contains fields 'question' and 'answers'
    and 'correctAnswer', which are optional.
    """
    question: Optional[str]
    answers: Optional[Dict[str, str]]
    correctAnswer: Optional[str]

    class Config:
        """
        This class shows how should request look like.
        """
        schema_extra = {
            "example": {
                "Question": "What kind of bear is best?",
                "answers": {'A': "That's a ridiculous question.",
                            'B': "Black bear"},
                "correctAnswer": 'B'
            }
        }


def response_model(data, message):
    """
    This function returns data and code 200 for successful request.
    :param data: dictionary.
    :param message: response message.
    """
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

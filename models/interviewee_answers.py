"""
This file contains:
    IntervieweeAnswers class.
"""
from pydantic import BaseModel


class IntervieweeAnswers(BaseModel):
    """
    This class is model for interviewee answer. It contains fields 'question_id' and 'answer',
    which are required.
    """
    question_id: str
    answer: str

    class Config:
        """
        This class shows how should request look like.
        """
        schema_extra = {
            "example": {
                "question_id": '624c4d993922d0c5d2c54108',
                "answer": 'B'
            }
        }

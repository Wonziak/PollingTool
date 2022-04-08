"""
This file contains:
    FeedbackForm class,
    UpdateFeedbackForm class,
    and response_model function.
"""
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class FeedbackForm(BaseModel):
    """
    This class is model for Feedback form. It contains fields 'title' and 'summary'
    which are required.
    """
    title: str = Field(min_length=1, max_length=50)
    summary: str = Field(min_length=1, max_length=500)

    class Config:
        """
        This class shows how should request look like.
        """
        schema_extra = {
            "example": {
                "title": 'Title of feedback',
                "summary": 'This is excellent!'
            }
        }


class UpdateFeedbackForm(BaseModel):
    """
    This class is model for updating Feedback form. It contains fields 'title' and 'summary',
    both are optional.
    """
    title: Optional[str]
    summary: Optional[str]

    class Config:
        """
        This class shows how should request look like.
        """
        schema_extra = {
            "example": {
                "title": 'Title of feedback',
                "summary": 'This is excellent!'
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

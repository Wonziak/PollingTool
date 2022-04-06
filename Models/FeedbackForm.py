from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional


class FeedbackForm(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    summary: str = Field(min_length=1, max_length=500)

    class Config:
        schema_extra = {
            "example": {
                "title": 'Title of feedback',
                "summary": 'This is excellent!'
            }
        }


class UpdateFeedbackForm(BaseModel):
    title: Optional[str]
    summary: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": 'Title of feedback',
                "summary": 'This is excellent!'
            }
        }


def response_model(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

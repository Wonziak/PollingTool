from pydantic import BaseModel


class IntervieweeAnswers(BaseModel):
    question_id: str
    answer: str

    class Config:
        schema_extra = {
            "example": {
                "question_id": '624c4d993922d0c5d2c54108',
                "answer": 'B'
            }
        }

"""
This application allows users to create polls - questions with answers to that questions.
User that wants to answer a question uses question id and choose one answer.

This app also allows users to create feedback.

All routes and descriptions are available on localhost:8080/docs.
"""
import uvicorn
from fastapi import FastAPI

from routers.question_router import question_router
from routers.interviewee_router import interviewee_router
from routers.feedback_router import feedback_router

app = FastAPI()
app.include_router(question_router)
app.include_router(interviewee_router)
app.include_router(feedback_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)

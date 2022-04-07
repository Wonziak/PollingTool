import uvicorn
from fastapi import FastAPI

from Routers.question_router import questionrouter
from Routers.interviewee_router import interviewee_router
from Routers.feedback_router import feedback_router

app = FastAPI()
app.include_router(questionrouter)
app.include_router(interviewee_router)
app.include_router(feedback_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)

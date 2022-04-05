import uvicorn
from fastapi import FastAPI

from Routers.questions_router import questionrouter
from Routers.user_router import userrouter
app = FastAPI()
app.include_router(questionrouter)
app.include_router(userrouter)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)

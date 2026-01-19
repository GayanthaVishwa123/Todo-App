from typing import List

from fastapi import Body, FastAPI

from .routers.taskrouters import router as task_router
from .routers.userrouters import router as user_router

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Todo API is running 🚀"}

from typing import List

import models
from fastapi import Body, FastAPI

from todo_backend.core.database import engine
from todo_backend.routers.taskrouters import router as task_router
from todo_backend.routers.userrouters import router as user_router

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Todo API is running 🚀"}


models.Base.metadata.create_all(bind=engine)

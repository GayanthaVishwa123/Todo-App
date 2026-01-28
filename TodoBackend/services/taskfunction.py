# from typing import Annotated

# from fastapi import Depends, HTTPException
# from sqlalchemy.orm import Session

# from ..models.todo import Task


# def completeTask(task: Annotated[dict, Depends()]):


#     # task start Date
#     if not task["complete_status"]:
#         taskStart_date = task["start_datetime"]
#         print("task_date: ", taskStart_date)

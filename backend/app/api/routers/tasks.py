from fastapi import APIRouter
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService, get_task_service
from fastapi import Depends
from app.db.base import Task
from uuid import UUID

router = APIRouter()

def get_task_helper(task: Task):
    if task is None:
        return {"error": "Task Not Found"}
    else:
        return {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "estimated_duration": task.estimated_duration,
            "deadline": task.deadline,
            "category_id": task.category_id,
            "project_id": task.project_id,
            "kind": task.kind,
            "is_flexible": task.is_flexible,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
    
@router.post("/user/{us_id}/task", tags=["tasks"])
async def create_task(
    us_id: int, 
    Task: TaskCreate, 
    service: TaskService = Depends(get_task_service)
    ):
    await service.create_task(us_id=us_id, task=Task)

@router.patch("/user/{us_id}/task/{task_id}", tags=["tasks"])
async def update_task(
    us_id: int,
    task_id: int,
    task: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    return await service.update_task(us_id=us_id, task_id=task_id, task_data=task)

@router.get("/user/{us_id}/task/{task_id}", tags=["tasks"])
async def get_task_mh(
    us_id: int, 
    task_id: int, 
    service: TaskService = Depends(get_task_service)
    ):
    res = await service.get_task(us_id=us_id, task_id=task_id)
    return get_task_helper(res)

@router.delete("/user/{us_id}/task/{task_id}", tags=["delete"])
async def soft_delete_mh(us_id: int, task_id: int, service: TaskService = Depends(get_task_service)):
    res = await service.soft_delete_task(us_id=us_id, task_id=task_id)
    return res


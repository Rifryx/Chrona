from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.project_service import ProjectService, get_project_service
from app.db.base import Project

router = APIRouter()

def project_to_dict(project: Project) -> dict[str, Any]:
    return {
        "id": project.id,
        "user_id": project.user_id,
        "title": project.title,
        "description": project.description,
        "status": project.status,
        "completed_at": project.completed_at,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "deleted_at": project.deleted_at,
    }

@router.post("/user/{us_id}/project", tags=["projects"])
async def create_project(
    us_id: int,
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    try:
        result = await service.create_project(us_id=us_id, project=project)
        return project_to_dict(result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/user/{us_id}/projects", tags=["projects"])
async def get_projects(
    us_id: int,
    service: ProjectService = Depends(get_project_service),
):
    result = await service.get_projects(us_id=us_id)
    return [project_to_dict(item) for item in result]

@router.get("/user/{us_id}/project/{project_id}", tags=["projects"])
async def get_project(
    us_id: int,
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    result = await service.get_project(us_id=us_id, project_id=project_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project_to_dict(result)

@router.patch("/user/{us_id}/project/{project_id}", tags=["projects"])
async def update_project(
    us_id: int,
    project_id: int,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    try:
        result = await service.update_project(us_id=us_id, project_id=project_id, project_data=project)
        return project_to_dict(result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.delete("/user/{us_id}/project/{project_id}", tags=["projects"])
async def soft_delete_project(
    us_id: int,
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    try:
        result = await service.soft_delete_project(us_id=us_id, project_id=project_id)
        return project_to_dict(result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete("/user/{us_id}/project/{project_id}/hard", tags=["projects"])
async def harsh_delete_project(
    us_id: int,
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    try:
        return await service.harsh_delete_project(us_id=us_id, project_id=project_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService, get_category_service
from app.db.base import Category

router = APIRouter()

def category_to_dict(category: Category) -> dict[str, Any]:
    return {
        "id": category.id,
        "user_id": category.user_id,
        "name": category.name,
        "icon": category.icon,
        "color": category.color,
        "created_at": category.created_at,
        "updated_at": category.updated_at,
        "deleted_at": category.deleted_at,
    }


@router.post("/user/{us_id}/category", tags=["categories"])
async def create_category(
    us_id: int,
    category: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    try:
        result = await service.create_category(user_id=us_id, category=category)
        return category_to_dict(result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/user/{us_id}/categories/defaults", tags=["categories"])
async def create_default_categories(
    us_id: int,
    service: CategoryService = Depends(get_category_service),
):
    try:
        await service.create_default_categories(user_id=us_id)
        return {"user_id": us_id, "defaults_created": True}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/user/{us_id}/categories", tags=["categories"])
async def get_categories(
    us_id: int,
    service: CategoryService = Depends(get_category_service),
):
    result = await service.get_categories(user_id=us_id)
    return [category_to_dict(item) for item in result]


@router.get("/user/{us_id}/category/{categ_id}", tags=["categories"])
async def get_category(
    us_id: int,
    categ_id: int,
    service: CategoryService = Depends(get_category_service),
):
    result = await service.get_category(user_id=us_id, categ_id=categ_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category_to_dict(result)


@router.patch("/user/{us_id}/category/{categ_id}", tags=["categories"])
async def update_category(
    us_id: int,
    categ_id: int,
    category: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    try:
        result = await service.update_categories(us_id=us_id, categ_id=categ_id, category_data=category)
        return category_to_dict(result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/user/{us_id}/category/{categ_id}", tags=["categories"])
async def soft_delete_category(
    us_id: int,
    categ_id: int,
    service: CategoryService = Depends(get_category_service),
):
    try:
        result = await service.soft_delete_category(us_id=us_id, categ_id=categ_id)
        return category_to_dict(result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/user/{us_id}/category/{categ_id}/hard", tags=["categories"])
async def harsh_delete_category(
    us_id: int,
    categ_id: int,
    service: CategoryService = Depends(get_category_service),
):
    try:
        return await service.harsh_delete_category(us_id=us_id, categ_id=categ_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

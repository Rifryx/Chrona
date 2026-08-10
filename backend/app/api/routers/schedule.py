from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.services.planning_service import PlanningService, get_planning_service
from app.services.schedule_service import ScheduleService, get_schedule_service
from app.schemas.schedule_block import ScheduleBlockCreate, ScheduleBlockUpdate

router = APIRouter()

@router.get("/user/{us_id}/daily-plan/{date_str}", tags=["schedule"])
async def get_daily_plan(
    us_id: int,
    date_str: str,
    schedule_service: ScheduleService = Depends(get_schedule_service),
):
    try:
        plan_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    daily_plan = await schedule_service.get_daily_plan(us_id, plan_date)
    if daily_plan is None:
        raise HTTPException(status_code=404, detail="Daily plan not found")

    blocks = await schedule_service.get_schedule_blocks_for_day(us_id, plan_date)

    return {
        "daily_plan": {
            "id": daily_plan.id,
            "user_id": daily_plan.user_id,
            "date": str(daily_plan.date),
            "status": daily_plan.status,
        },
        "schedule_blocks": [
            {
                "id": block.id,
                "task_id": block.task_id,
                "start_time": str(block.start_time),
                "end_time": str(block.end_time),
                "order_index": block.order_index,
            }
            for block in blocks
        ],
    }

@router.post("/user/{us_id}/daily-plan/{date_str}/generate", tags=["schedule"])
async def generate_daily_plan(
    us_id: int,
    date_str: str,
    planning_service: PlanningService = Depends(get_planning_service),
    schedule_service: ScheduleService = Depends(get_schedule_service),
):
    try:
        plan_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    daily_plan = await planning_service.build_daily_plan(us_id, plan_date)
    blocks = await schedule_service.get_schedule_blocks_for_day(us_id, plan_date)

    return {
        "daily_plan": {
            "id": daily_plan.id,
            "user_id": daily_plan.user_id,
            "date": str(daily_plan.date),
            "status": daily_plan.status,
        },
        "schedule_blocks": [
            {
                "id": block.id,
                "task_id": block.task_id,
                "start_time": str(block.start_time),
                "end_time": str(block.end_time),
                "order_index": block.order_index,
            }
            for block in blocks
        ],
    }

@router.post("/user/{us_id}/daily-plan/{daily_plan_id}/block", tags=["schedule"])
async def create_schedule_block(
    us_id: int,
    daily_plan_id: int,
    block_data: ScheduleBlockCreate,
    schedule_service: ScheduleService = Depends(get_schedule_service),
):
    block = await schedule_service.create_schedule_block(daily_plan_id, block_data)
    return {
        "id": block.id,
        "task_id": block.task_id,
        "start_time": str(block.start_time),
        "end_time": str(block.end_time),
        "order_index": block.order_index,
    }

@router.patch("/user/{us_id}/schedule-block/{block_id}", tags=["schedule"])
async def update_schedule_block(
    us_id: int,
    block_id: int,
    block_data: ScheduleBlockUpdate,
    schedule_service: ScheduleService = Depends(get_schedule_service),
):
    block = await schedule_service.update_schedule_block(us_id, block_id, block_data)
    return {
        "id": block.id,
        "task_id": block.task_id,
        "start_time": str(block.start_time),
        "end_time": str(block.end_time),
        "order_index": block.order_index,
    }

@router.delete("/user/{us_id}/schedule-block/{block_id}", tags=["schedule"])
async def delete_schedule_block(
    us_id: int,
    block_id: int,
    schedule_service: ScheduleService = Depends(get_schedule_service),
):
    block = await schedule_service.soft_delete_schedule_block(us_id, block_id)
    return {"deleted": True, "block_id": block.id}
from fastapi import APIRouter
from app.services.user_serv import UserService
router = APIRouter()

@router.get('/user/{telegram_id}')
async def get_user(telegram_id: int):
    user = await UserService.get_user(telegram_id)
    if user is None:
        return {"error": "User not found"}
    else:
        return {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "subscription_plan": user.subscription_plan.value,
            "subscription_started_at": user.subscription_started_at,
            "subscription_until": user.subscription_until,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "tz": user.tz
        }

from datetime import datetime, date, time, timedelta
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from app.services.settings_service import SettingsService
from app.services.schedule_service import ScheduleService
from app.db.base import ScheduleBlock, DailyPlan, Task, TaskStatus, TaskKind, Priority
from app.schemas.schedule_block import ScheduleBlockCreate
from app.db.session import session_factory

def get_planning_service():
    return PlanningService()

class PlanningService():
    @staticmethod
    async def _get_settings(us_id: int):
        settings = await SettingsService.get_settings(us_id=us_id)
        if settings is None:
            raise ValueError("user settings not found")
        return settings

    @staticmethod
    async def _get_task_to_schedule(us_id: int):
        async with session_factory() as session:
            res = await session.execute(select(Task).where(
                Task.user_id==us_id,
                Task.status==TaskStatus.TODO,
                Task.deleted_at.is_(None),
                Task.kind==TaskKind.TASK
            ))
            return res.scalars().all()
    @staticmethod
    async def _get_fixied_events(user_id: int, date: date):
        async with session_factory() as session:
            res = await session.execute(select(Task).where(
                Task.user_id==user_id,
                Task.deleted_at.is_(None),
                Task.kind==TaskKind.EVENT,
                Task.is_flexible==False
            ))
            return res.scalars().all()

    @staticmethod
    async def _calculate_free_intervals( settings, events):
        free_intervals = [
            {
                "start": settings.planning_start,
                "end": settings.planning_end
            }
        ]
        if not events:
            return free_intervals
        events.sort(key=lambda e: e.start_time)
        result = []
        for interval in free_intervals:
            current_start = interval["start"]
            for event in events:
                if event.end_time <= current_start or event.start_time >= interval["end"]:
                    continue
                if event.start_time > current_start:
                    result.append({
                        "start": current_start,
                        "end": event.start_time
                    })
                current_start = max(current_start, event.end_time)
            if current_start < interval["end"]:
                result.append({
                    "start": current_start,
                    "end": interval["end"]
                })
        return result
    @staticmethod
    async def _sort_tasks( tasks):
        priority_order = {
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3
        }
        return sorted(
            tasks,
            key=lambda e: (
                priority_order.get(e.priority, 999),
                e.deadline if e.deadline else datetime.max
            )
        )
    
    @staticmethod
    async def _allocate_tasks( sorted_tasks, free_intervals):
    
        allocations = []
        order_index = 1
        
        for task in sorted_tasks:
            # Для каждой задачи ищем подходящий интервал
            allocated = False
            
            for i, interval in enumerate(free_intervals):
                # Считаем, сколько минут свободно в интервале
                start_time = interval["start"]
                end_time = interval["end"]
                
                # Длительность в минутах
                duration_minutes = int(
                    (end_time.hour * 60 + end_time.minute) -
                    (start_time.hour * 60 + start_time.minute)
                )
                
                # Проверяем, поместится ли задача
                if duration_minutes >= task.estimated_duration:
                    # ДА, создаём блок
                    allocations.append({
                        "task_id": task.id,
                        "start_time": start_time,
                        "end_time": (
                            start_time.replace(
                                hour=start_time.hour + task.estimated_duration // 60,
                                minute=start_time.minute + task.estimated_duration % 60
                            )
                        ),
                        "order_index": order_index,
                    })
                    
                    # Сокращаем интервал или удаляем его
                    if duration_minutes > task.estimated_duration:
                        # Осталось ещё время
                        remaining_minutes = duration_minutes - task.estimated_duration
                        new_start_hour = start_time.hour + task.estimated_duration // 60
                        new_start_minute = start_time.minute + task.estimated_duration % 60
                        
                        free_intervals[i]["start"] = time(new_start_hour, new_start_minute)
                    else:
                        # Интервал исчерпан, удаляем
                        free_intervals.pop(i)
                    
                    order_index += 1
                    allocated = True
                    break
            
            # Если задача не поместилась, она просто пропускается
            # (остаётся в tasks как не спланированная)
        
        return allocations
    
    @staticmethod
    async def _create_blocks( daily_plan_id: int, allocations: list):
        for allocation in allocations:
            block_create = ScheduleBlockCreate(
                task_id=allocation["task_id"],
                start_time=allocation["start_time"],
                end_time=allocation["end_time"],
                order_index=allocation["order_index"]
            )
            await ScheduleService.create_schedule_block(
                daily_plan_id=daily_plan_id,
                schedule=block_create
            )
    @staticmethod
    async def build_daily_plan(self, user_id: int, date: date) -> DailyPlan:
        
        # Шаг 1: Получить или создать план на день
        daily_plan = await ScheduleService.get_or_create_daily_plan(user_id, date)
        
        # Шаг 2: Очистить старые блоки (если регенерируем)
        await ScheduleService.delete_schedule_blocks_for_plan(daily_plan.id)
        
        # Шаг 3: Собрать данные
        settings = await self._get_settings(user_id)
        tasks = await self._get_tasks_to_schedule(user_id)
        events = await self._get_fixed_events(user_id, date)
        
        # Шаг 4: Логика планирования (чистая функция, без БД)
        free_intervals = self._calculate_free_intervals(settings, events)
        sorted_tasks = self._sort_tasks(tasks)
        allocations = self._allocate_tasks(sorted_tasks, free_intervals)
        
        # Шаг 5: Сохранить результат в БД
        await self._create_blocks(daily_plan.id, allocations)
        
        # Шаг 6: Вернуть готовый план
        return daily_plan


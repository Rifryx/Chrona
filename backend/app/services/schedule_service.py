from datetime import datetime, date, time
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from app.schemas.schedule_block import ScheduleBlockCreate, ScheduleBlockUpdate
from app.db.base import ScheduleBlock, DailyPlan
from app.db.session import session_factory

def get_schedule_service():
    return ScheduleService()

class ScheduleService():
    @staticmethod
    async def get_daily_plan(us_id: int, date: date) -> DailyPlan | None:
        async with session_factory() as session:
            res = await session.execute(select(DailyPlan).where(
                DailyPlan.user_id==us_id, DailyPlan.date==date, DailyPlan.deleted_at.is_(None)
            ))
            return res.scalar_one_or_none()
    @staticmethod
    async def get_or_create_daily_plan(user_id: int, date: date) -> DailyPlan:
        plan = await ScheduleService.get_daily_plan(us_id=user_id, date=date)
        if plan is not None:
            return plan
        
        async with session_factory() as session:
            new_plan = DailyPlan(
                user_id=user_id,
                date=date,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(new_plan)
            try:
                await session.commit()
                await session.refresh(new_plan)
                return new_plan
            except IntegrityError:
                await session.rollback()
                plan = await ScheduleService.get_daily_plan(us_id=user_id, date=date)
                if plan is not None:
                    return plan
                raise ValueError("daily pan not created sue to integrity error")
        return plan
    @staticmethod
    async def get_schedule_blocks_for_day(user_id: int, date: date) -> list[ScheduleBlock]:
        async with session_factory() as session:
            res = (
                select(ScheduleBlock)
                .join(DailyPlan, ScheduleBlock.daily_plan_id==DailyPlan.id)
                .where(DailyPlan.user_id==user_id,
                       DailyPlan.date==date,
                       ScheduleBlock.deleted_at.is_(None))
                       .order_by(ScheduleBlock.order_index)

            )
            result = await session.execute(res)
            return list(result.scalars().all())
    @staticmethod
    async def get_schedule_block_by_id(user_id: int, block_id: int)-> ScheduleBlock | None:
        async with session_factory() as session:
            res = await session.execute(select(ScheduleBlock).join(
                DailyPlan, ScheduleBlock.daily_plan_id==DailyPlan.id
            )
            .where(DailyPlan.user_id == user_id,
                   ScheduleBlock.id==block_id,
                   ScheduleBlock.deleted_at.is_(None))
            )
            return res.scalar_one_or_none()
    @staticmethod
    async def create_schedule_block(daily_plan_id: int, schedule: ScheduleBlockCreate) -> ScheduleBlock:
        async with session_factory() as session:
            new_schedule = ScheduleBlock(
                daily_plan_id=daily_plan_id,
                task_id=schedule.task_id,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                order_index=schedule.order_index
            )
            session.add(new_schedule)
            try:
                await session.commit()
                await session.refresh(new_schedule)
                return new_schedule
            except IntegrityError:
                await session.rollback()
                raise ValueError("schedule block not created due to integrity error")

    @staticmethod
    async def update_schedule_block(user_id: int, block_id: int, block_data: ScheduleBlockUpdate) -> ScheduleBlock:
        updated_data = {
            key: value for key, value in block_data.model_dump(exclude_unset=True).items()
        }
        if not updated_data:
            exis = await ScheduleService.get_schedule_block_by_id(user_id=user_id, block_id=block_id)
            if exis is None:
                raise ValueError("block not found")
            return exis
        async with session_factory() as session:
            res = await session.execute(select(ScheduleBlock).join(
                        DailyPlan, ScheduleBlock.daily_plan_id==DailyPlan.id
                    )
                    .where(DailyPlan.user_id == user_id,
                            ScheduleBlock.id==block_id,
                            ScheduleBlock.deleted_at.is_(None))
                    )
            exis = res.scalar_one_or_none()
            if exis is None:
                raise ValueError("block not found")
            for key, value in updated_data.items():
                setattr(exis, key, value)
            exis.updated_at = datetime.utcnow()
            try:
                await session.commit()
                await session.refresh(exis)
                return exis
            except IntegrityError:
                await session.rollback()
                raise ValueError("Scheduleblock not update due to integrity error")
            
            
    @staticmethod
    async def soft_delete_schedule_block(user_id: int, block_id: int) -> ScheduleBlock:
        async with session_factory() as session:
            res = await session.execute(select(ScheduleBlock).join(
                            DailyPlan, ScheduleBlock.daily_plan_id==DailyPlan.id
                        )
                        .where(DailyPlan.user_id == user_id,
                               ScheduleBlock.id==block_id,
                               ScheduleBlock.deleted_at.is_(None))
                        )
            block = res.scalar_one_or_none()
            if block is None:
                raise ValueError("block not found")

            block.deleted_at = datetime.utcnow()
            block.updated_at = datetime.utcnow()
            try:
                await session.commit()
                await session.refresh(block)
                return block
            except IntegrityError:
                await session.rollback()
                raise ValueError("block not update due to integrity error")
            

    @staticmethod
    async def delete_schedule_blocks_for_plan(daily_plan_id: int) -> None:
        async with session_factory() as session:
            res = await session.execute(select(ScheduleBlock).where(
                ScheduleBlock.daily_plan_id==daily_plan_id))
            blocks = res.scalars().all()
            if not blocks:
                return
            for block in blocks:
                await session.delete(block)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("block not delete")
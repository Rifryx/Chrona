from datetime import datetime
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.db.base import Category
from app.db.session import session_factory


def get_category_service():
    return CategoryService()


class CategoryService:
    @staticmethod
    async def create_category(user_id: int, category: CategoryCreate) -> Category:
        async with session_factory() as session:
            new_category = Category(
                user_id=user_id,
                name=category.name,
                icon=category.icon,
                color=category.color,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(new_category)
            try:
                await session.commit()
                await session.refresh(new_category)
                return new_category
            except IntegrityError:
                await session.rollback()
                raise ValueError("Category creation failed due to integrity error.")

    @staticmethod
    async def get_category(user_id: int, categ_id: int) -> Category | None:
        async with session_factory() as session:
            result = await session.execute(
                select(Category).where(Category.user_id == user_id, Category.id == categ_id, Category.deleted_at.is_(None))
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def get_categories(user_id: int) -> list[Category]:
        async with session_factory() as session:
            result = await session.execute(select(Category).where(Category.user_id == user_id, Category.deleted_at.is_(None)))
            return result.scalars().all()

    @staticmethod
    async def update_categories(us_id: int, categ_id: int, category_data: CategoryUpdate) -> Category:
        update_data: dict[str, Any] = {
            key: value for key, value in category_data.model_dump().items()
            if key in category_data.model_fields_set
        }
        if not update_data:
            exs = await CategoryService.get_category(us_id, categ_id)
            if exs is None:
                raise ValueError("Category not found")
            return exs

        update_data["updated_at"] = datetime.utcnow()
        async with session_factory() as session:
            res = await session.execute(select(Category).where(Category.id == categ_id, Category.user_id == us_id, Category.deleted_at.is_(None)))
            exs = res.scalar_one_or_none()
            if exs is None:
                raise ValueError("Category not found")
            await session.execute(
                update(Category)
                .where(Category.user_id == us_id, Category.id == categ_id)
                .values(**update_data)
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Category update failed due to integrity error.")
            await session.refresh(exs)
            return exs

    @staticmethod
    async def soft_delete_category(us_id: int, categ_id: int) -> Category:
        async with session_factory() as session:
            res = await session.execute(select(Category).where(Category.id == categ_id, Category.user_id == us_id))
            exis = res.scalar_one_or_none()
            if exis is None:
                raise ValueError("Category not found")
            await session.execute(
                update(Category).where(Category.id == categ_id, Category.user_id == us_id).values(deleted_at=datetime.utcnow())
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Category soft delete failed due to integrity error.")
            await session.refresh(exis)
            return exis

    @staticmethod
    async def harsh_delete_category(us_id: int, categ_id: int) -> dict[str, int | bool]:
        async with session_factory() as session:
            res = await session.execute(select(Category).where(Category.id == categ_id, Category.user_id == us_id, Category.deleted_at.is_not(None)))
            exs = res.scalar_one_or_none()
            if exs is None:
                raise ValueError("Soft deleted category not found")
            await session.delete(exs)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Category deletion failed due to integrity error.")
            return {"category_id": categ_id, "deleted": True}

    @staticmethod
    async def create_default_categories(user_id: int, session: AsyncSession | None = None) -> None:
        default_categories = [
            Category(
                user_id=user_id,
                name="Учёба",
                icon="book",
                color="#6366F1",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            Category(
                user_id=user_id,
                name="Работа",
                icon="briefcase",
                color="#0EA5E9",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            Category(
                user_id=user_id,
                name="Спорт",
                icon="gym",
                color="#10B981",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            Category(
                user_id=user_id,
                name="Дом",
                icon="home",
                color="#F59E0B",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            Category(
                user_id=user_id,
                name="Развлечения",
                icon="star",
                color="#EC4899",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]
        if session is not None:
            session.add_all(default_categories)
            return

        async with session_factory() as session:
            session.add_all(default_categories)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Default categories creation failed due to integrity error.")


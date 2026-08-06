from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from app.db.base import Category, User
from app.db.session import session_factory
from app.services.category_service import CategoryService


class UserService:
    

    @staticmethod
    async def get_user(tg_id: int) -> User | None:
        async with session_factory() as session:
            result = await session.execute(select(User).where(User.telegram_id == tg_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(user_id: int) -> User | None:
        async with session_factory() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def create_user(tg_id: int, username: str | None, first_name: str | None) -> User:
        async with session_factory() as session:
            new_user = User(
                telegram_id=tg_id,
                username=username,
                first_name=first_name,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(new_user)

            try:
                await session.flush()
                await CategoryService.create_default_categories(new_user.id, session=session)
                await session.commit()
                await session.refresh(new_user)
                return new_user
            except IntegrityError:
                await session.rollback()
                raise ValueError("User with this telegram_id already exists.")

    @staticmethod
    async def get_or_create(tg_id: int, username: str | None, first_name: str | None) -> tuple[User, bool]:
        user = await UserService.get_user(tg_id)
        if user is not None:
            return user, False
        try:
            return await UserService.create_user(tg_id, username, first_name), True
        except (IntegrityError, ValueError):
            existing = await UserService.get_user(tg_id)
            if existing is None:
                raise
            return existing, False

    @staticmethod
    async def get_tg_id(user_id: int) -> int | None:
        async with session_factory() as session:
            result = await session.execute(select(User.telegram_id).where(User.id == user_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def set_tz(tg_id: int, tz: str) -> None:
        async with session_factory() as session:
            await session.execute(
                update(User)
                .where(User.telegram_id == tg_id)
                .values(tz=tz, updated_at=datetime.utcnow())
            )
            await session.commit()

    @staticmethod
    async def get_tz(tg_id: int) -> str | None:
        async with session_factory() as session:
            result = await session.execute(select(User.tz).where(User.telegram_id == tg_id))
            return result.scalar_one_or_none()

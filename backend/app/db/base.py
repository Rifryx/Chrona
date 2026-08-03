from datetime import date, datetime, time
import enum

import sqlalchemy as sa
from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, JSON, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"


class ProjectStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskKind(str, enum.Enum):
    TASK = "task"
    EVENT = "event"


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        sa.Enum(SubscriptionPlan, name="subscriptionplan"),
        default=SubscriptionPlan.FREE,
        server_default=SubscriptionPlan.FREE.value,
    )
    subscription_started_at: Mapped[datetime | None]
    subscription_until: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", server_default="UTC")
    planning_start: Mapped[time | None] = mapped_column(Time)
    planning_end: Mapped[time | None] = mapped_column(Time)
    profile_description: Mapped[str | None] = mapped_column(Text)
    weekly_schedule_json: Mapped[dict | None] = mapped_column(JSON)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True, server_default=sa.true())
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    icon: Mapped[str | None] = mapped_column(String(255))
    color: Mapped[str | None] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ProjectStatus] = mapped_column(
        sa.Enum(ProjectStatus, name="projectstatus"),
        default=ProjectStatus.ACTIVE,
        server_default=ProjectStatus.ACTIVE.value,
    )
    completed_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[Priority] = mapped_column(
        sa.Enum(Priority, name="priority"),
        default=Priority.MEDIUM,
        server_default=Priority.MEDIUM.value,
    )
    estimated_duration: Mapped[int | None] = mapped_column(Integer)
    deadline: Mapped[datetime | None] = mapped_column(DateTime)
    kind: Mapped[TaskKind] = mapped_column(
        sa.Enum(TaskKind, name="taskkind"),
        default=TaskKind.TASK,
        server_default=TaskKind.TASK.value,
    )
    is_flexible: Mapped[bool] = mapped_column(Boolean, default=True, server_default=sa.true())
    status: Mapped[TaskStatus] = mapped_column(
        sa.Enum(TaskStatus, name="taskstatus"),
        default=TaskStatus.TODO,
        server_default=TaskStatus.TODO.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)


class DailyPlan(Base):
    __tablename__ = "daily_plans"
    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_daily_plans_user_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[datetime] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(32), default="active", server_default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)

class ScheduleBlock(Base):
    __tablename__ = "schedule_blocks"
    __table_args__ = (UniqueConstraint("daily_plan_id", "order_index", name="uq_schedule_blocks_plan_order"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    daily_plan_id: Mapped[int] = mapped_column(ForeignKey("daily_plans.id", ondelete="CASCADE"))
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    order_index: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)

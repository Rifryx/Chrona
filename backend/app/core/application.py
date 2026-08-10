from fastapi import FastAPI
from app.api.routers import (
    health, users, tasks, projects,
    planner, ai, settings, categories,
    schedule
)

def register_routers(app: FastAPI):
    app.include_router(health.router)
    app.include_router(users.router)
    app.include_router(tasks.router)
    app.include_router(categories.router)
    app.include_router(projects.router)
    app.include_router(settings.router)
    app.include_router(schedule.router)


def create_app() -> FastAPI:
    app = FastAPI()

    register_routers(app)

    return app


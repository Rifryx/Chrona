from fastapi import FastAPI
from app.api.routers import (
    health, users, tasks, projects,
    planner, ai, settings, categories,
)

def register_routers(app: FastAPI):
    app.include_router(health.router)
    app.include_router(users.router)
    app.include_router(tasks.router)
    
    

def create_app() -> FastAPI:
    app = FastAPI()

    register_routers(app)

    return app


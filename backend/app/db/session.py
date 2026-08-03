from app.db.enums import engine
from sqlalchemy.ext.asyncio import async_sessionmaker

session_factory = async_sessionmaker(
    engine, 
    expire_on_commit=False
    )

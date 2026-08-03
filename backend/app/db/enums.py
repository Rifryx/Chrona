from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from sqlalchemy import event

engine = create_async_engine(settings.DATABASE_URL, echo=False)


if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine.sync_engine, "connect")
    def _enable_sqlite_fk(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()



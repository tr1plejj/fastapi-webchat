from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

database_url = 'sqlite+aiosqlite:///db.sqlite3'
async_engine = create_async_engine(url=database_url)
async_session = async_sessionmaker(async_engine)


class Base(AsyncAttrs, DeclarativeBase):
    """Основной класс для моделей."""

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
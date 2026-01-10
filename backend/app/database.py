import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base

# By default, writes to data/warehouse.db in the cwd
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/warehouse.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

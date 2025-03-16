from typing import Any
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# ================================================
# aiosqlite in-memory database
# ================================================
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# ================================================
# DB Session dependency
# ================================================
async def get_db() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

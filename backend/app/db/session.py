from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from base import Base

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

#Init db tables in main
async def init_db():

    import models.book, models.rental, models.user
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Async dependency to get a DB session
async def get_db():

    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

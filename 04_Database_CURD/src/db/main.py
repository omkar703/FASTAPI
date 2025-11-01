from typing import AsyncGenerator
from sqlmodel import text , SQLModel
from sqlalchemy.ext.asyncio import create_async_engine , AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession 
from sqlalchemy.orm import sessionmaker 

engine = create_async_engine(
    url = Config.DATABASE_URL.replace("postgresql", "postgresql+asyncpg"),
    echo=True # able to see all sql logs || production = False
)


async def init_db() -> None:
    async with engine.begin() as conn:
         from src.books.Models import Book
         # Create the database tables
         await conn.run_sync(Book.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind = engine,
        class_= AsyncSession,
        expire_on_commit= False
    )
    async with Session() as session:
        async with session.begin():
            yield session
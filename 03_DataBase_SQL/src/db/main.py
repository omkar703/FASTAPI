from sqlmodel import text , SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config


engine = create_async_engine(
    url = Config.DATABASE_URL.replace("postgresql", "postgresql+asyncpg"),
    echo=True # able to see all sql logs || production = False
)


async def init_db():
    async with engine.begin() as conn:
         from src.books.Models import Book
         # Create the database tables
         await conn.run_sync(Book.metadata.create_all)
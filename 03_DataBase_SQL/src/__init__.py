from fastapi import FastAPI 
from src.books.routes import router_book
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    await init_db()
    yield
    print("Shutting down application...")


version = "1v"

app = FastAPI(
    version=version,
    title="Book Management API",
    description="A simple API to manage books using FastAPI",
    lifespan=lifespan

)

app.include_router(router_book , prefix=f"/api/{version}/books", tags=["books"])
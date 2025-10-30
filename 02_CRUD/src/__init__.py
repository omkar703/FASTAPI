from fastapi import FastAPI 
from src.books.routes import router_book

version = "1v"

app = FastAPI(
    version=version,
    title="Book Management API",
    description="A simple API to manage books using FastAPI",

)

app.include_router(router_book , prefix=f"/api/{version}/books", tags=["books"])
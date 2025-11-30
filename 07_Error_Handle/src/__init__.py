from ast import In
from fastapi import FastAPI , status , HTTPException
from src.books.routes import router_book
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router 
from src.error import InvalidToken , UserAlreadyExists, create_exception_handler


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

app.add_exception_handler(UserAlreadyExists, 
                          create_exception_handler(
                              status_code=status.HTTP_409_CONFLICT,
                              initial_detail={"error": f"{UserAlreadyExists.__name__}User already exists"}
                          ))

app.add_exception_handler(InvalidToken, 
                          create_exception_handler(
                              status_code=status.HTTP_401_UNAUTHORIZED,
                              initial_detail={"error": f"{InvalidToken.__name__}Invalid token"}
                          ))

app.include_router(router_book , prefix=f"/api/{version}/books", tags=["books"])

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])

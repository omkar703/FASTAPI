from typing import Any , Callable # funtion for the return error handler
from fastapi import Request 
from fastapi.responses import JSONResponse
class BooklyException(Exception):
    "This is the base class for all bookly errors"
    pass

class InvalidToken(BooklyException):
    "user provided provided an invalid or expired error"
    pass

class UsersException(Exception):
    "This is the base class for all user errors"
    pass

class UserAlreadyExists(UsersException):
    "This is raised when the user already exists"
    pass


def create_exception_handler(status_code : int , initial_detail: Any ) -> Callable[[Request , Exception], JSONResponse]:
    async def exception_handler(request : Request , exc : Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={"error": initial_detail}
        )
   
    return exception_handler
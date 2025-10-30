from fastapi import FastAPI , Header 
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get("/" ,status_code=200)
async def read_root():
    return {"message": "Hello, World!"}


# here the query parameter is age
@app.get('/greet/{name}')
async def greet(name: str , age : int):
    return {"message": f"Hello, {name}! You are {age} years old."}


# name query parameter example
# here it's endpoint: /welcome/?name=YourName
@app.get('/welcome/')
# here we can able to specify the return type as dict
async def welcome(name: str = "Guest") -> dict:
    return {"message": f"Welcome, {name}!"}



@app.get('/names/')
async def get_names(names: Optional[str] = None ,
                    age : int = 0) -> dict:
    if names:
        name_list = names.split(',')
        return {"names": name_list, "age": age}
    return {"message": f"No names provided. Age is {age}."}
    


# for the POST request validation of the data 
class BookCreateModel(BaseModel):
    title: str
    author: str
    year: int

@app.post('/create_book')
async def create_book(book: BookCreateModel) -> dict:
    return {"message": f"Book '{book.title}' created successfully!"}


@app.get('/get_headers')
async def get_headers(
    accept: str = Header(None),
    content_type : str = Header(None),  
    user_agent: str = Header(None),
    host: str = Header(None)
    ) -> dict:

    request_headers = {}

    request_headers['accept'] = accept
    request_headers['content_type'] = content_type
    request_headers['user_agent'] = user_agent
    request_headers['host'] = host
    return {"headers": request_headers}

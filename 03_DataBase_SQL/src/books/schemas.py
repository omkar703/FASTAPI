from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: int
    publisher: str
    page_count: int
    language: str


class UpdateBookModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
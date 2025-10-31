from fastapi import APIRouter, HTTPException, status
from typing import List
from src.books.schemas import Book, UpdateBookModel
from src.books.book_data import books


router_book = APIRouter()

@router_book.get("/" , response_model=list[Book])
async def get_all_books() -> List[Book]:
    return books

@router_book.get("/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router_book.post("/" , status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book) -> dict:
    # model_dump() is used to convert pydantic model to dictionary
    new_book = book_data.model_dump()
    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}



#PATCH method to update a book because we are updating only few fields but if we use post or put method then we have to provide all fields and if we miss any field then it will be set to null or default value 
@router_book.patch("/{book_id}")
async def update_a_book(book_id: int, book_update_data:  UpdateBookModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            update_data = book_update_data.model_dump(exclude_unset=True)
            book.update(update_data)
            return {"message": "Book updated successfully", "book": book}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router_book.delete("/{book_id}" , status_code=status.HTTP_200_OK)
async def delete_a_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
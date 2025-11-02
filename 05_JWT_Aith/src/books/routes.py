from fastapi import APIRouter, HTTPException, status , Depends
from typing import List
from src.books.schemas import Book, CreateBookModel, UpdateBookModel
from src.books.book_data import books
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession 
from src.db.main import get_session


router_book = APIRouter()
book_service = BookService()

@router_book.get("/" , response_model=list[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)) -> List[Book]:
    return await book_service.get_all_books(session)

@router_book.get("/{book_id}", response_model=Book)
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)) -> Book:
    book = await book_service.get_book_by_id(book_id, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router_book.post("/" , status_code=status.HTTP_201_CREATED , response_model=Book)
async def create_a_book(book_data:CreateBookModel, session: AsyncSession = Depends(get_session)) -> Book:
    new_book = await book_service.create_book(book_data, session)
    return new_book



#PATCH method to update a book because we are updating only few fields but if we use post or put method then we have to provide all fields and if we miss any field then it will be set to null or default value 
@router_book.patch("/{book_id}", response_model=Book)
async def update_a_book(book_id: str, book_update_data:  UpdateBookModel, session: AsyncSession = Depends(get_session)) -> Book:
    updated_book = await book_service.update_book(book_id, book_update_data, session)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return updated_book


@router_book.delete("/{book_id}" , status_code=status.HTTP_200_OK)
async def delete_a_book(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    deleted = await book_service.delete_book(book_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"message": "Book deleted successfully"}
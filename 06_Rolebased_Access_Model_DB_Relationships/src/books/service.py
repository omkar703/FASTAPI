from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import CreateBookModel , UpdateBookModel
from sqlmodel import select ,desc
from .Models import Book

class BookService:
    async def get_all_books(self, session : AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        results = await session.exec(statement)
        books = results.all()
        return books

    async def get_book_by_id(self, book_id : str, session : AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        results = await session.exec(statement)
        book = results.first()
        return book

    async def create_book(self, book_data : CreateBookModel, session : AsyncSession):
        new_book =  Book.model_validate(book_data)
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(self, book_id : str, update_data : UpdateBookModel, session : AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        results = await session.exec(statement)
        book_to_update = results.first()
        if not book_to_update:
            return f"Book with id {book_id} not found"
        update_data_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)
        session.add(book_to_update)
        await session.commit()
        return book_to_update

    async def delete_book(self, book_id, session : AsyncSession):
        delete_statement = select(Book).where(Book.uid == book_id)
        results = await session.exec(delete_statement)
        book_to_delete = results.first()
        if not book_to_delete:
            return f"Book with id {book_id} not found"
        await session.delete(book_to_delete)
        await session.commit()  
        return {"message": f"Book with id {book_id} deleted successfully"}

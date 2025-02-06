import uuid

from fastapi import Depends

from app.repositories.book_repository import BookRepository, get_book_repository
from app.schemas.book import BookCreate, BookUpdate


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    async def get_books(self):
        return await self.book_repository.get_books()

    async def get_book(self, id: uuid.UUID):
        return await self.book_repository.find_by_id(id)

    async def create_book(self, book: BookCreate):
        return await self.book_repository.create(book.model_dump())

    async def update_book(self, id: uuid.UUID, book: BookUpdate):
        return await self.book_repository.update(id, book.model_dump())

    async def delete_book(self, id: uuid.UUID):
        return await self.book_repository.soft_delete(id)


def get_book_service(repository: BookRepository = Depends(get_book_repository)) -> BookService:
    return BookService(repository)

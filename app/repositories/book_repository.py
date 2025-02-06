import uuid
from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.models import Book


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_books(self):
        stmt = select(Book).where(Book.deleted_at.is_(None))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def find_by_id(self, id: uuid.UUID) -> Optional[Book]:
        stmt = select(Book).where(Book.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Book:
        record = Book(**data)

        self.db.add(record)
        try:
            await self.db.commit()
            await self.db.refresh(record)
            return record
        except IntegrityError:
            await self.db.rollback()
            raise

    async def update(self, id: uuid.UUID, data: dict) -> Book:
        book = await self.find_by_id(id)
        if not book:
            raise ValueError("Book not found.")

        for key, value in data.items():
            setattr(book, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(book)
            return book
        except IntegrityError:
            await self.db.rollback()
            raise

    async def soft_delete(self, id: uuid.UUID) -> Book:
        book = await self.find_by_id(id)
        if not book:
            raise ValueError("Book not found.")

        book.deleted_at = datetime.utcnow()

        try:
            await self.db.commit()
            await self.db.refresh(book)
            return book
        except IntegrityError:
            await self.db.rollback()
            raise


def get_book_repository(db: AsyncSession = Depends(get_db)) -> BookRepository:
    return BookRepository(db)

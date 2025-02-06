import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.book_service import BookService, get_book_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookRead])
async def get_books(service: BookService = Depends(get_book_service)):
    return await service.get_books()


@router.get("/{id}", response_model=BookRead)
async def get_book(id: uuid.UUID, service: BookService = Depends(get_book_service)):
    book = await service.get_book(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("/", response_model=BookRead)
async def create_book(book: BookCreate, service: BookService = Depends(get_book_service)):
    return await service.create_book(book)


@router.put("/{id}", response_model=BookRead)
async def update_book(id: uuid.UUID, book: BookUpdate, service: BookService = Depends(get_book_service)):
    return await service.update_book(id, book)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: uuid.UUID, service: BookService = Depends(get_book_service)):
    try:
        await service.delete_book(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return Response(status_code=204)

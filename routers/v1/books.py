from typing import Annotated

from sqlalchemy import delete, select, update
from models.sellers import Seller
from routers.v1.auth import authenticate_token

from schemas.books import IncomingBook, ReturnedAllBooks, ReturnedBook
from fastapi import HTTPException, status, APIRouter, Depends
from configurations.database import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from models.books import Book

books_router = APIRouter(
    tags=["books"],
    prefix="/books"
)

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

# Ручка для создания записи о книге в БД. Возвращает созданную книгу.
@books_router.post("/", response_model=ReturnedBook, status_code=status.HTTP_201_CREATED)  # Прописываем модель ответа
async def create_book(book: IncomingBook, session: DBSession, email: str = Depends(authenticate_token)):  # прописываем модель валидирующую входные данные
    # Check if the seller_id exists
    seller = await session.execute(select(Seller).where(Seller.id == book.seller_id))
    if not seller.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid seller_id")
    new_book = Book(
        title = book.title,
        author = book.author,
        year = book.year,
        count_pages = book.count_pages,
        seller_id = book.seller_id
    )
    session.add(new_book)
    await session.flush()

    # return new_book  # Так можно просто вернуть объект
    return new_book


# Ручка, возвращающая все книги
@books_router.get("/", response_model=ReturnedAllBooks)
async def get_all_books(session: DBSession):
    # Хотим видеть формат:
    # books: [{"id": 1, "title": "Blabla", ...}, {"id": 2, ...}]
    query = select(Book)
    res = await session.execute(query)
    books = res.scalars().all()
    return {"books": books}


# Ручка для получения книги по ее ИД
@books_router.get("/{book_id}", response_model=ReturnedBook)
async def get_book(book_id: int, session: DBSession):
    query = select(Book).filter_by(id=book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(status_code=404, detail="id does not exist")

    return book


# Ручка для удаления книги
@books_router.delete("/{book_id}")
async def delete_book(book_id: int, session: DBSession):
    query = delete(Book).filter_by(id=book_id)
    await session.execute(query)
    return book_id


# Ручка для обновления данных о книге
@books_router.put("/{book_id}")
async def update_book(book_id: int, book: IncomingBook, session: DBSession, email: str = Depends(authenticate_token)):
    query = update(Book).where(Book.id == book_id).values(
        author=book.author, 
        title=book.title, 
        count_pages=book.count_pages, 
        year=book.year)
    result = await session.execute(query)
    updated_row_count = result.rowcount
    await session.commit()
    return updated_row_count

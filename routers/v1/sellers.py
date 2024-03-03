from typing import Annotated

from sqlalchemy import delete, select, update
from routers.v1.auth import authenticate_token

from schemas.sellers import ReturnedSeller, IncomingSeller, ReturnedAllSellers
from fastapi import HTTPException, status, APIRouter, Depends
from configurations.database import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from models.sellers import Seller

sellers_router = APIRouter(
    tags=["sellers"],
    prefix="/sellers"
)

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

@sellers_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: IncomingSeller, session: DBSession):
    new_seller = Seller(
        first_name = seller.first_name,
        last_name = seller.last_name,
        e_mail = seller.e_mail,
        password = seller.password,
        books = list()
    )
    session.add(new_seller)
    await session.flush()

    return new_seller

@sellers_router.get("/{seller_id}", response_model=ReturnedSeller)
async def get_seller(seller_id: int, session: DBSession, email: str = Depends(authenticate_token)):
    query = select(Seller).join(Seller.books, isouter=True).options(contains_eager(Seller.books)).where(Seller.id == seller_id)
    result = await session.execute(query)
    seller = result.unique().scalar_one_or_none()

    if seller is None:
        raise HTTPException(status_code=404, detail="id does not exist")
    
    return seller

@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    query = select(Seller).join(Seller.books, isouter=True).options(contains_eager(Seller.books))
    res = await session.execute(query)
    sellers = res.unique().scalars().all()
    return {"sellers": sellers}

@sellers_router.delete("/{seller_id}")
async def delete_seller(seller_id: int, session: DBSession):
    query = delete(Seller).filter_by(id=seller_id)
    result = await session.execute(query)
    return result.scalar_one_or_none

@sellers_router.put("/{seller_id}")
async def update_seller(seller_id: int, seller: IncomingSeller, session: DBSession):
    query = update(Seller).where(Seller.id == seller_id).values(
        first_name = seller.first_name,
        last_name = seller.last_name,
        e_mail = seller.e_mail,
        password=seller.password)
    result = await session.execute(query)
    updated_row_count = result.rowcount
    await session.commit()
    return updated_row_count
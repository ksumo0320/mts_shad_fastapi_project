from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

from schemas.books import ReturnedBook


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    e_mail: str


class ReturnedSeller(BaseSeller):
    id: int
    books: list[ReturnedBook]


class IncomingSeller(BaseSeller):
    password: str


class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]
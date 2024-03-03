from typing import List

from models.books import Book
from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class Seller(BaseModel):
    __tablename__ = "sellers_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    e_mail: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    books: Mapped[List[Book]] = relationship("Book", backref="seller", uselist=True)
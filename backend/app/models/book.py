from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from .rental import Rental

class Author(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Genre(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="genre")


class Book(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    available_copies: Mapped[int] = mapped_column(Integer, default=1)

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"), nullable=False)

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
    rentals: Mapped[list["Rental"]] = relationship("Rental", back_populates="book")
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
# from datetime import datetime

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    name: Mapped[str]
    birth_date: Mapped[str]
    date_of_death: Mapped[str]

    def __repr__(self):
        return f"Author({self.author_id}, {self.name})"

    def __str__(self):
        return f"Author: {self.name} ID: {self.author_id} Birthday: {self.birth_date} Death: {self.date_of_death}"


class Book(db.Model):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    publication_year: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id"))

    def __repr__(self):
        return f"Book({self.title})"

    def __str__(self):
        return f"ID: {self.book_id} Book: {self.title} Year: {self.publication_year} ISBN: {self.isbn}"

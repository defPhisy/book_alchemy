import os
import typing
from datetime import datetime
from typing import List, Union

from data_models import Author, Book, db
from dummy_data import populate_dummy_data
from flask import Flask, flash, render_template, request

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = "./data"
DB_NAME = "library.sqlite"
FULL_DB_PATH = os.path.join(ROOT_PATH, DB_FOLDER, DB_NAME)

app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{FULL_DB_PATH}",
    SECRET_KEY=os.getenv("SECRET_KEY", "your-default-secret-key"),
)
db.init_app(app)

# create db tables based on data_models , called only once for table creation or database got cancelled
if not os.path.exists(FULL_DB_PATH):
    with app.app_context():
        db.create_all()

        # insert dummy data once
        populate_dummy_data()


@app.route("/")
def index() -> str:
    """
    The home page route for the application.

    This function handles sorting and searching books in the library.
    Displays the list of books along with the total count of books.

    :return: Rendered HTML template for the home page.
    :rtype: str
    """
    sort = Book.title  # default sorting

    if "sort" in request.args:
        sort: str = request.args["sort"]
    books = db_get_books(sort)

    if "search" in request.args:
        search = request.args["search"]
        search_results = db_search_books(search)
        print(search_results)
        if search_results:
            books = search_results
        else:
            error = "No books found!"
            flash(error)

    book_count = Book.count_books(db.session)
    return render_template("home.html", books=books, book_count=book_count)


@app.route("/add_author", methods=["GET", "POST"])
def add_author() -> str:
    """
    The route to add a new author.

    Handles both GET and POST requests. For GET, it renders the author
    addition form. For POST, it adds a new author to the database.

    :return: Rendered HTML template for adding an author or confirmation message.
    :rtype: str
    """
    if request.method == "POST":
        new_author = db_add_author(request.form)
        return render_template("message.html", item=new_author)

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book() -> str:
    """
    The route to add a new book.

    Handles both GET and POST requests. For GET, it renders the book
    addition form. For POST, it adds a new book to the database.

    :return: Rendered HTML template for adding a book or confirmation message.
    :rtype: str
    """
    if request.method == "POST":
        new_book = db_add_book(request.form)
        return render_template("message.html", item=new_book)

    authors = db_get_authors()
    current_year = datetime.now().year

    return render_template(
        "add_book.html", authors=authors, current_year=current_year
    )


@app.route("/book/<int:book_id>/delete", methods=["GET"])
def delete_book(book_id: int) -> Union[str, tuple[str, int]]:
    """
    The route to delete a book by its ID.

    Fetches the book from the database by its ID, deletes it if found,
    and renders a confirmation page.

    :param book_id: The ID of the book to delete.
    :type book_id: int
    :return: Rendered HTML template for deletion confirmation or error page.
    :rtype: str or tuple[str, int]
    """
    book = db.session.execute(
        db.select(Book).where(Book.book_id == book_id)
    ).scalar_one_or_none()

    if not book:
        return render_template("error.html", message="Book not found"), 404

    db.session.delete(book)
    db.session.commit()

    return render_template("delete_book.html", book=book)


def db_get_books(sort: str) -> List[Book]:
    """
    Fetches and sorts books from the database based on the given sort parameter.

    :param sort: The field to sort by (e.g., 'title', 'author', etc.).
    :type sort: str
    :return: A list of books sorted by the specified field.
    :rtype: List[Book]
    """
    sort_options = {
        "title": Book.title,
        "author": Author.name,
        "publication_year": Book.publication_year,
        "rating": Book.rating,
    }

    sort_by = sort_options.get(sort, Book.title)
    if sort == "rating":
        result = (
            (
                db.session.execute(
                    db.select(Book).join(Book.author).order_by(sort_by.desc())
                )
            )
            .scalars()
            .all()
        )
    else:
        result = (
            (
                db.session.execute(
                    db.select(Book).join(Book.author).order_by(sort_by)
                )
            )
            .scalars()
            .all()
        )
    return typing.cast(List[Book], result)


def db_search_books(search: str) -> List[Book]:
    """
    Searches for books by title using a case-insensitive substring match.

    :param search: The search term to look for in book titles.
    :type search: str
    :return: A list of books matching the search term.
    :rtype: List[Book]
    """
    search = f"%{search.lower()}%"
    result = (
        (db.session.execute(db.select(Book).where(Book.title.like(search))))
        .scalars()
        .all()
    )
    return typing.cast(List[Book], result)


def db_get_authors() -> List[Author]:
    """
    Fetches all authors from the database, sorted alphabetically by name.

    :return: A list of all authors.
    :rtype: List[Author]
    """
    result = (
        db.session.execute(db.select(Author).order_by(Author.name))
        .scalars()
        .all()
    )
    return typing.cast(List[Author], result)


def db_add_author(request: dict) -> Author:
    """
    Adds a new author to the database.

    :param request: A dictionary containing author details ('name', 'birthdate', etc.).
    :type request: dict
    :return: The newly added Author object.
    :rtype: Author
    """
    name: str = request.get("name", None)
    birth_date: str = request.get("birthdate", None)
    death_date: str = request.get("date_of_death", None)
    new_author = Author(
        name=name,  # type: ignore
        birth_date=birth_date,  # type: ignore
        date_of_death=death_date,  # type: ignore
    )

    db.session.add(new_author)
    db.session.commit()

    return new_author


def db_add_book(request) -> Book:
    """
    Adds a new book to the database.

    :param request: A dictionary containing book details ('title', 'isbn', etc.).
    :type request: dict
    :return: The newly added Book object.
    :rtype: Book
    :raises ValueError: If the specified author does not exist in the database.
    """
    title: str = request.get("title")
    isbn: str = request.get("isbn")
    author_id: str = request.get("author")
    pub_year: str = request.get("publication_year")
    summary: str = request.get("summary")
    img_url: str = request.get("img_url")
    rating: str = request.get("rating")

    # get author from author_name for author.id in book
    author = db.session.execute(
        db.select(Author).where(Author.id == int(author_id))
    ).scalar_one_or_none()

    if not author:
        raise ValueError("Author not found in database.")

    new_book = Book(
        title=title,  # type: ignore
        isbn=isbn,  # type: ignore
        publication_year=pub_year,  # type: ignore
        author_id=author.id,  # type: ignore
        summary=summary,  # type: ignore
        img_url=img_url,  # type: ignore
        rating=rating,  # type: ignore
    )

    db.session.add(new_book)
    db.session.commit()

    return new_book


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

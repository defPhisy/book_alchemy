from flask import Flask, render_template, request
from data_models import db, Book, Author
import os
from datetime import datetime

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = "./data"
DB_NAME = "library.sqlite"
FULL_DB_PATH = os.path.join(ROOT_PATH, DB_FOLDER, DB_NAME)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{FULL_DB_PATH}"
db.init_app(app)

# create db tables based on data_models , called only once for table creation
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    if request.args:
        sort = request.args["sort"]
    else:
        sort = Book.title

    books = db_get_books(sort)
    book_count = Book.count_books(db.session)
    return render_template("home.html", books=books, book_count=book_count)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        new_author = db_add_author(request.form)
        return render_template("message.html", item=new_author)

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        new_book = db_add_book(request.form)
        return render_template("message.html", item=new_book)

    authors = db_get_authors()
    current_year = datetime.now().year

    return render_template(
        "add_book.html", authors=authors, current_year=current_year
    )


@app.route("/book/<int:book_id>/delete", methods=["GET"])
def delete_book(book_id):
    book = db.session.execute(
        db.select(Book).where(Book.book_id == book_id)
    ).scalar_one_or_none()

    if not book:
        return render_template("error.html", message="Book not found"), 404

    db.session.delete(book)
    db.session.commit()

    return render_template("delete_book.html", book=book)


def db_get_books(sort):
    sort_options = {
        "title": Book.title,
        "author": Author.name,
        "publication_year": Book.publication_year,
        "rating": Book.rating,
    }

    sort_by = sort_options.get(sort, Book.title)
    if sort == "rating":
        return (
            db.session.execute(
                db.select(Book).join(Book.author).order_by(sort_by.desc())
            )
        ).scalars()

    return (
        db.session.execute(db.select(Book).join(Book.author).order_by(sort_by))
    ).scalars()


def db_get_authors():
    return db.session.execute(
        db.select(Author).order_by(Author.name)
    ).scalars()


def db_add_author(request) -> Author:
    name: str = request.get("name")
    birth_date: str = request.get("birthdate")
    death_date: str = request.get("date_of_death")
    new_author = Author(
        name=name,  # type: ignore
        birth_date=birth_date,  # type: ignore
        date_of_death=death_date,  # type: ignore
    )

    db.session.add(new_author)
    db.session.commit()

    return new_author


def db_add_book(request) -> Book:
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

from flask import Flask, render_template, request
from data_models import db, Book, Author


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.sqlite"
db.init_app(app)

# create db tables based on data_models , called only once for table creation
# with app.app_context():
#     db.create_all()


@app.route("/")
def index():
    books = db_get_books()
    return render_template("home.html", books=books)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        new_author = db_add_author(request.form)
        return render_template("message.html", new_author=new_author)

    return render_template("add_author.html")


def db_get_books():
    return db.session.execute(
        db.select(Book, Author)
        .join(Author, Author.author_id == Book.author_id)
        .order_by(Book.title)
    ).all()


def db_add_author(request) -> Author:
    name: str = request.get("name")
    birth_date: str = request.get("birthdate")
    death_date: str = request.get("date_of_death")
    new_author = Author(
        name=name, birth_date=birth_date, date_of_death=death_date
    )
    db.session.add(new_author)
    db.session.commit()

    return new_author


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

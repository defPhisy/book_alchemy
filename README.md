# Library Management App

A Flask-based web application for managing books and authors in a library. Users can add, search, and delete books, as well as view and add authors.

## Features

- View all books with sorting options by title, author, publication year, or rating.
- Search books by title.
- Add new authors and books to the library.
- Delete books from the library.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/defPhisy/book_alchemy.git
cd book_alchemy
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
flask run --host=0.0.0.0 --port=5002
```

The app will be available at http://127.0.0.1:5002.
And create a SQLite database (library.sqlite) in the ./data folder and populate it with dummy data if not existing.

## Technologies

Flask: Web framework for Python.

SQLAlchemy: ORM for database interaction.

SQLite: Database for storing book and author data.

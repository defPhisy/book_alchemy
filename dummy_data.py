"""Populate new Database with dummy Data"""

from data_models import Author, Book, db


def populate_authors() -> None:
    author_data = {
        "name": "J.K. Rowling",
        "birth_date": "1965-07-31",
        "date_of_death": None,
    }
    new_author = Author(**author_data)
    db.session.add(new_author)
    db.session.commit()


def populate_books(author) -> None:
    books_data = [
        {
            "isbn": 9780747532699,
            "title": "Harry Potter and the Philosopher's Stone",
            "publication_year": "1997",
            "author_id": author.id,
            "summary": "Harry discovers he's a wizard on his 11th birthday and attends Hogwarts School of Witchcraft and Wizardry.",
            "img_url": "https://m.media-amazon.com/images/I/81m9fP+LIPL._SL1500_.jpg",
            "rating": 5,
        },
        {
            "isbn": 9780747538493,
            "title": "Harry Potter and the Chamber of Secrets",
            "publication_year": "1998",
            "author_id": author.id,
            "summary": "Harry returns to Hogwarts for his second year and discovers the mystery of the Chamber of Secrets.",
            "img_url": "https://m.media-amazon.com/images/I/81Wbfijio4L._SL1500_.jpg",
            "rating": 4,
        },
        {
            "isbn": 9780747542155,
            "title": "Harry Potter and the Prisoner of Azkaban",
            "publication_year": "1999",
            "author_id": author.id,
            "summary": "Harry learns that the fugitive Sirius Black, believed to be responsible for his parents' deaths, is after him.",
            "img_url": "https://m.media-amazon.com/images/I/81y-3oSkxGL._SL1500_.jpg",
            "rating": 5,
        },
        {
            "isbn": 9780747546245,
            "title": "Harry Potter and the Goblet of Fire",
            "publication_year": "2000",
            "author_id": author.id,
            "summary": "Harry competes in the dangerous Triwizard Tournament, where he faces deadly challenges.",
            "img_url": "https://m.media-amazon.com/images/I/81YoazRCtBL._SL1500_.jpg",
            "rating": 3,
        },
        {
            "isbn": 9780747551003,
            "title": "Harry Potter and the Order of the Phoenix",
            "publication_year": "2003",
            "author_id": author.id,
            "summary": "Harry fights against the Ministry of Magic's refusal to acknowledge Voldemort’s return, while facing his own inner turmoil.",
            "img_url": "https://m.media-amazon.com/images/I/816DPd8HNBL._SL1500_.jpg",
            "rating": 5,
        },
        {
            "isbn": 9780747581083,
            "title": "Harry Potter and the Half-Blood Prince",
            "publication_year": "2005",
            "author_id": author.id,
            "summary": "Harry uncovers secrets about Voldemort's past and his weaknesses as he prepares for the ultimate battle.",
            "img_url": "https://m.media-amazon.com/images/I/813zbNPhO5L._SL1500_.jpg",
            "rating": 5,
        },
        {
            "isbn": 9780747591051,
            "title": "Harry Potter and the Deathly Hallows",
            "publication_year": "2007",
            "author_id": author.id,
            "summary": "Harry, Ron, and Hermione set out on a quest to destroy Voldemort’s Horcruxes and defeat him in the final battle.",
            "img_url": "https://m.media-amazon.com/images/I/81qmfY6mMrL._SL1500_.jpg",
            "rating": 2,
        },
    ]
    for book_data in books_data:
        new_book = Book(**book_data)
        db.session.add(new_book)
        db.session.commit()


def populate_dummy_data():
    populate_authors()
    author = db.session.query(Author).filter_by(name="J.K. Rowling").first()
    populate_books(author)

from sqlalchemy.orm import Session
from models import Book
from schemas import BookBase
from ddtrace import tracer

@tracer.wrap("create-book")
def create_book(db: Session, book: BookBase, log):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    log.info("Creating book", book=book.title)
    return new_book

@tracer.wrap("get-books")
def get_all_books(db: Session, log):
    books = db.query(Book).all()
    log.info("Querying books")
    return books

@tracer.wrap("get-book")
def get_book(db: Session, book_id: int, log):
    book  = db.query(Book).filter(Book.id == book_id).first()
    log.info("Querying book", book_id=book_id)
    return book

@tracer.wrap("update-books")
def update_book(db: Session, book_id: int, book_data: BookBase,log):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        for key, value in book_data.dict().items():
            setattr(book, key, value)
        db.commit()
    log.info("Updating book", book=book.title)
    return book

@tracer.wrap("update-books")
def delete_book(db: Session, book_id: int, log):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    log.info("Deleting book", book_id= book_id)
    return book

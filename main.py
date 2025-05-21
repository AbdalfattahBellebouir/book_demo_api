from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import BookBase, BookResponse
from repository import book as book_repo
import models
from log_struct import setup_structlog
import structlog

models.Base.metadata.create_all(bind=engine)
setup_structlog()
log = structlog.get_logger()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/")
def create_book(book: BookBase, db: Session = Depends(get_db)):
    log.info("Got create book request", book= book.title)
    b = book_repo.create_book(db, book, log)
    log.info("Done create the book", book= book.title)
    return b

@app.get("/books/")
def read_books(db: Session = Depends(get_db)):
    log.info("Got get books request")
    books = book_repo.get_all_books(db, log)
    log.info("Done querying books")
    return books

@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    log.info("Got get a book request", book_id= book_id)
    book = book_repo.get_book(db, book_id, log)
    if not book:
        log.error("Failed to get the book", book_id= book_id)
    else:
        log.info("Done querying the book", book_id= book_id)
        return book

@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookBase, db: Session = Depends(get_db)):
    log.info("Got update book request", book_id= book_id)
    updated = book_repo.update_book(db, book_id, book, log)
    if not updated:
        log.error("Failed to update the book", book_id= book_id)
    else:
        log.info("Done updating the book", book_id= book_id)
        return updated

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    log.info("Got delete book request", book= book_id)
    deleted = book_repo.delete_book(db, book_id, log)
    if not deleted:
        log.error("failed to delete book", book_id=book_id)
        return {"ok": False}
    else:
        log.info("book deleted", book_id=book_id)
        return {"ok": False}

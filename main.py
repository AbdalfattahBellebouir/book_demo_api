import time
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import BookBase, BookResponse
from repository import book as book_repo
import models
from log_struct import setup_structlog
import structlog
import logging
import sys
from log_struct import inject_trace_ids, setup_structlog
from fastapi.middleware.cors import CORSMiddleware
from ddtrace import tracer, config, patch_all

models.Base.metadata.create_all(bind=engine)

patch_all()

setup_structlog()

logger = structlog.get_logger()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@tracer.wrap("post-books", service="post-books-api")
@app.post("/books/")
def create_book(book: BookBase, db: Session = Depends(get_db)):
    logger.info("Got create book request", book= book.title)
    b = book_repo.create_book(db, book, logger)
    logger.info("Done create the book", book= book.title)
    return b

@tracer.wrap("get-books", service="get-books-api")
@app.get("/books/")
def read_books(db: Session = Depends(get_db)):
    logger.info("Got get books request")
    books = book_repo.get_all_books(db, logger)
    logger.info("Done querying books")
    return books

@tracer.wrap("get-book", service="get-book-api")
@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    logger.info("Got get a book request", book_id= book_id)
    book = book_repo.get_book(db, book_id, logger)
    if not book:
        logger.error("Failed to get the book", book_id= book_id)
    else:
        logger.info("Done querying the book", book_id= book_id)
        return book

@tracer.wrap("update-book", service="update-book-api")
@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookBase, db: Session = Depends(get_db)):
    logger.info("Got update book request", book_id= book_id)
    updated = book_repo.update_book(db, book_id, book, logger)
    if not updated:
        logger.error("Failed to update the book", book_id= book_id)
    else:
        logger.info("Done updating the book", book_id= book_id)
        return updated

@tracer.wrap("delete-book", service="delete-book-api")
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    logger.info("Got delete book request", book= book_id)
    deleted = book_repo.delete_book(db, book_id, logger)
    if not deleted:
        logger.error("failed to delete book", book_id=book_id)
        return {"ok": False}
    else:
        logger.info("book deleted", book_id=book_id)
        return {"ok": False}

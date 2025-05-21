from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    year: int

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True

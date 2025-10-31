from sqlmodel import SQLModel, Field , Column
from datetime import datetime
import uuid 
import sqlalchemy.dialects.postgresql as pg

class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid : uuid.UUID = Field(
        sa_column= Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            default=uuid.uuid4()
        )
    )
    title: str
    author: str
    published_year: int
    publisher: str
    page_count: int
    language: str
    created_at: datetime = Field(Column(pg.TIMESTAMP(timezone=True), default=datetime.now()))
    updated_at: datetime = Field(Column(pg.TIMESTAMP(timezone=True), default=datetime.now(), onupdate=datetime.now()))


    def __repr__(self):
        return f"<Book {self.title} >"


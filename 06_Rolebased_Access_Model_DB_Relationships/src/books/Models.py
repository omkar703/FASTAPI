from token import OP
from sqlmodel import SQLModel, Field , Column , Relationship
from datetime import datetime
import uuid 
import sqlalchemy.dialects.postgresql as pg
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.models import User

class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid : uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column= Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    published_year: int
    publisher: str
    page_count: int
    language: str
    created_at: datetime = Field(default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now))
    user_uid : Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    user : Optional["User"] = Relationship(back_populates="books")


    def __repr__(self):
        return f"<Book {self.title} >"


from sqlmodel import SQLModel , Field , Column
import uuid 
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg



# for the user we can create the model to authenticate the user 

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid : uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column= Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=100, unique=True, index=True)
    password_hash: str = Field(exclude=True) # exclude means when we convert from datatype then it will hide values 
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now))

    def __repr__(self):
        return f"<User {self.username} >"
 

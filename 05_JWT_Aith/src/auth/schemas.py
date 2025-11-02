from pydantic import BaseModel , Field
import uuid
from datetime import datetime

class UserCreateModel(BaseModel):
    first_name : str = Field(max_length=50)
    last_name : str = Field(max_length=50)
    username: str = Field(max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(min_length=6)


class UserModel(BaseModel):
    uid : uuid.UUID 
    username: str 
    email: str 
    password_hash: str = Field(exclude=True)
    first_name: str 
    last_name: str 
    is_verified: bool 
    created_at: datetime 
    updated_at: datetime 


class UserLoginModel(BaseModel):
    email: str = Field(max_length=100)
    password: str = Field(min_length=6)
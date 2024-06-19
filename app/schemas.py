# app/schemas.py
from pydantic import BaseModel ,ConfigDict

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode: True
    

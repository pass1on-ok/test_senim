from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ReportCreate(BaseModel):
    category: str
    message: str

class ReportOut(BaseModel):
    id: int
    category: str
    message: str
    created_at: datetime
    author: UserOut

    class Config:
        from_attributes = True

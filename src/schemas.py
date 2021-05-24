from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

# Task Classes
class TaskBase(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime]

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int   #put in another class if not used elsewhere

    class Config:
        orm_mode = True

# User Classes

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    task: List[Task] = []

    class Config:
        orm_mode = True
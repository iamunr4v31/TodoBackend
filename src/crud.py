from typing import List
from icecream import ic
import pydantic

from sqlalchemy.orm import Session
from datetime import datetime

from passlib.hash import bcrypt

import models, schemas


def get_user(db: Session, user_id: int)-> models.User or None:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):  #type hint return type later
    return db.query(models.User).filter(models.User.email == email).first()

# def get_users(db: Session, skip: int = 0, lim: int = 100)-> List[models.User]:
#     return db.query(models.User).offset(skip).limit(lim).all()

def validate_password(db: Session, email: str)-> bool:
    return db.query(models.User).filter(models.User.email == email).first().hashed_password

def authenticate_user(db: Session, password: str, email: str)-> bool:
    if get_user_by_email(db, email):
        hashed_pass = validate_password(db=db, email=email)
        return bcrypt.verify(password, hashed_pass)
    return False

def create_user(db: Session, user: schemas.UserCreate)-> schemas.User:
    hashed_password = bcrypt.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks(db: Session, user_id: int)-> List[models.Task]:
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    # mytime = datetime
    db_task = models.Task(title=task.title, description=task.description, due_dateTime=task.due_dateTime, owner_id=user_id)
    db.add(db_task)
    ic(db_task.__dict__)
    db.commit()
    task1 = db.query(models.Task).filter(models.Task.id == db_task.id).first()
    # task1.due_dateTime = task1.due_dateTime.isoformat()
    # ic(task1.__dict__)
    
    # ic(db_task.__dict__)
    # db.refresh(db_task)
    return task1
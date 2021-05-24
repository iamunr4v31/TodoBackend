from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import logging

# from os import path

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///database/todo.db'

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
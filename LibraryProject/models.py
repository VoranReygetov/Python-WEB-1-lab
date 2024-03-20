from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, DateTime, create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

from fastapi import FastAPI
#connect db
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                       connect_args={"check_same_thread": False})

Base = declarative_base()

class Authors(Base):
    __tablename__ = "Authors"

    id = Column(Integer, primary_key=True, index=True)
    nameAuthor = Column(String)
    surnameAuthor = Column(String)

class Categories(Base):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True, index=True)
    nameCategories = Column(String, nullable=False)

class Books(Base):
    __tablename__ ="Books"
    id = Column(Integer, primary_key=True, index=True)
    nameBook = Column(String, nullable=False)
    yearBook = Column(Integer)
    availableBook = Column(Integer)
    category_id = Column(Integer, ForeignKey("Categories.id"))
    author_id = Column(Integer, ForeignKey("Authors.id"))

class User(Base):
    __tablename__ ="Users"
    id = Column(Integer, primary_key=True, index=True)
    nameUser = Column(String, nullable=False)
    surnameUser = Column(String)
    passwordUser = Column(String, nullable=False)
    is_admin = Column(Boolean, default= False)
    emailUser = Column(String, nullable=False, unique=True)
    numberUser = Column(Integer)

class History(Base):
    __tablename__ ="History"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    books_id = Column(Integer, ForeignKey("Books.id"), nullable=False)
    dateLoan = Column(DateTime, nullable=False)
    dateReturn = Column(DateTime)
    isReturned = Column(Boolean, default= False)

    #table
    
SessionLocal = sessionmaker(autoflush=False, bind=engine)


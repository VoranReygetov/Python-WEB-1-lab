from sqlalchemy.orm import sessionmaker
from models import *
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

Base.metadata.create_all(bind=engine)

db = SessionLocal()
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()  
# author = Authors(id=1, nameAuthor="Test", surnameAuthor="Test")
# db.add(author)
# db.commit()

# print(author.nameAuthor)
authors = db.query(Authors).all()
for author in authors:
    print(f"{author.nameAuthor} {author.surnameAuthor}")
from sqlalchemy.orm import sessionmaker
from models import *
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()     #uvicorn main:app --reload
# db = SessionLocal()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return FileResponse("templates/login.html")

@app.post("/")
def main():
    return FileResponse("templates/login.html")

@app.get("/registration")
def register_page():
    return FileResponse("templates/registration.html")

@app.post("/registration")
def create_user(data = Body(), db: User = Depends(get_db)):
    user = User(nameUser=data["nameUser"], surnameUser=data["surnameUser"],
                  passwordUser=data["passwordUser"],emailUser=data["emailUser"],numberUser=data["numberUser"])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/book-list")
def book_list_page():
    return FileResponse("templates/book-list.html")

@app.post("/book-list")
def book_list_page(data = Body(), db: Books = Depends(get_db)):
    book = Books(id=data["id"], nameBook=data["nameBook"],
                  yearBook=data["yearBook"],availableBook=data["availableBook"],category_id=data["category_id"],
                  author_id=data["author_id"])
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
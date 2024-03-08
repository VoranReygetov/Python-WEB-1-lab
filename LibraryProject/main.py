from sqlalchemy.orm import sessionmaker
from models import *
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse, HTMLResponse
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

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
def book_list_page(db: Books = Depends(get_db)):
    book_list_page = env.get_template('book-list.html')
    output = book_list_page.render(books=db.query(Books).all())
    return HTMLResponse(output)

@app.post("/book-list")
def book_post_page(data = Body(), db: Books = Depends(get_db)):
    book = Books(id=data["id"], nameBook=data["nameBook"],
                  yearBook=data["yearBook"],availableBook=data["availableBook"],category_id=data["category_id"],
                  author_id=data["author_id"])
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.post("/authors")
def authors_post_page(data = Body(), db: Authors = Depends(get_db)):
    author = Authors(id=data["id"], nameAuthor=data["nameAuthor"],
                  surnameAuthor=data["surnameAuthor"])
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

@app.post("/categoies")
def categories_post_page(data = Body(), db: Categories = Depends(get_db)):
    category = Categories(id=data["id"], nameCategories=data["nameCategories"])
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
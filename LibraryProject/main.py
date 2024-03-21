from sqlalchemy.orm import sessionmaker, Session
from models import *
from fastapi import Depends, FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse, HTMLResponse
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

Base.metadata.create_all(bind=engine)
app = FastAPI()     #uvicorn main:app --reload

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return RedirectResponse("/login")

@app.get("/login")
def main():
    return FileResponse("templates/login.html")

@app.post("/login")
def login(data = Body(), db: Session = Depends(get_db)):
    email = data.get("emailUser")
    password = data.get("passwordUser")
    searched_user = db.query(User).filter_by(emailUser=email).first()
    if searched_user and searched_user.passwordUser == password:
        return searched_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed")

@app.get("/registration")
def register_page():
    return FileResponse("templates/registration.html")

@app.post("/registration")
def create_user(data = Body(), db: Session = Depends(get_db)):
    user = User(nameUser=data["nameUser"], surnameUser=data["surnameUser"],
                  passwordUser=data["passwordUser"],emailUser=data["emailUser"],numberUser=data["numberUser"])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/book-list")
def book_list_page(db: Session = Depends(get_db)):
    book_list_page = env.get_template('book-list.html')
    output = book_list_page.render(books=db.query(Book).all())
    return HTMLResponse(output)

@app.get("/book/{book_id}")
def book_list_page(book_id, db: Session = Depends(get_db)):
    book =  db.query(Book).filter(Book.id == book_id).first()     # якщо не знайдений, відправляємо статусний код і повідомлення про помилку
    if book==None:
        return JSONResponse(status_code=404, content={ "message": "Книжка не знайдена"})        #якщо користувача знайдено, відправляємо його
    return book

@app.post("/book")
def book_post_page(book_data = Body(), db: Session = Depends(get_db)):
    book = Book(
        nameBook=book_data.get("nameBook"),
        yearBook=book_data.get("yearBook"),
        availableBook=book_data.get("availableBook"),
        category_id=book_data.get("category_id"),
        author_id=book_data.get("author_id")
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.put("/book")
def edit_person(data = Body(), db: Session = Depends(get_db)):
    # отримуємо користувача за id
    book = db.query(Book).filter(Book.id == data["id"]).first()
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку
    if book == None:
        return JSONResponse(status_code=404, content={ "message": "Книжка не знайдена"})
    # якщо користувач знайдений, змінюємо його дані і відправляємо назад клієнту
    book.nameBook = data["nameBook"]
    book.yearBook = data["yearBook"]
    book.availableBook =  data["availableBook"]
    book.category_id =  data["category_id"]
    book.author_id =  data["author_id"]
    db.commit() # зберігаємо зміни
    db.refresh(book)
    return book

@app.delete("/book/{book_id}")
def delete_person(book_id, db: Session = Depends(get_db)):
    # отримуємо користувача за id
    book = db.query(Book).filter(Book.id == book_id).first()
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку
    if book == None:
        return JSONResponse( status_code=404, content={ "message": "Книжка не знайдена"})
    # якщо користувача знайдено, видаляємо його
    db.delete(book) # видаляємо об'єкт
    db.commit() # зберігаємо зміни
    return book

@app.post("/authors")
def authors_post_page(data: dict = Body(...), db: Session = Depends(get_db)):
    for category_data in data:
        nameAuthor = category_data.get("nameAuthor")
        surnameAuthor = category_data.get("surnameAuthor")
        author = Author(nameAuthor=nameAuthor, surnameAuthor = surnameAuthor)
        db.add(author)
    db.commit()
    db.refresh(author)
    return db.query(Author).all()

@app.post("/categories")
def categories_post_page(data: dict = Body(...), db: Session = Depends(get_db)):
    for category_data in data:
        category_name = category_data.get("nameCategory")
        category = Category(nameCategory=category_name)
        db.add(category)
    db.commit()
    db.refresh(category)
    return db.query(Category).all()

@app.post("/book-list")
def book_post_page(data: dict = Body(...), db: Session = Depends(get_db)):
    for book_data in data:
        book = Book(
            nameBook=book_data.get("nameBook"),
            yearBook=book_data.get("yearBook"),
            availableBook=book_data.get("availableBook"),
            category_id=book_data.get("category_id"),
            author_id=book_data.get("author_id")
        )
        db.add(book)
    db.commit()
    return db.query(Book).all()
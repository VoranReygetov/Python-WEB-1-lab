from sqlalchemy.orm import sessionmaker, Session, joinedload
from models import *
from fastapi import Depends, FastAPI, Body, HTTPException, status, Response, Cookie
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

def authenticate_user(db: Session, email: str, password: str):
    searched_user = db.query(User).filter_by(emailUser=email).first()
    if searched_user and searched_user.check_password(password):
        return searched_user
    return None

@app.get("/login")
def login_get(email: str| None = Cookie(default=None), password: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if user:
        return RedirectResponse("/book-list")
    return FileResponse("templates/login.html")
    
@app.post("/login")
def login(data = Body(), db: Session = Depends(get_db)):
    email = data.get("emailUser")
    password = data.get("passwordUser")
    searched_user = db.query(User).filter_by(emailUser=email).first()
    try:
        if searched_user.check_password(password):
            response = JSONResponse(content={"message": f"{searched_user}"})
            response.set_cookie(key="email", value=data.get("emailUser"))
            response.set_cookie(key="password", value=data.get("passwordUser"))
            return response
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed")

@app.get("/registration")
def register_page():
    return FileResponse("templates/registration.html")

@app.post("/registration")
def create_user(data = Body(), db: Session = Depends(get_db)):
    user = User(nameUser=data["nameUser"], surnameUser=data["surnameUser"],
                  passwordUser=data["passwordUser"],emailUser=data["emailUser"],numberUser=data["numberUser"])
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Registration failed")
    response = JSONResponse(content={"message": f"{user}"})
    response.set_cookie(key="email", value=data.get("emailUser"))
    response.set_cookie(key="password", value=data.get("passwordUser"))
    return response

@app.get("/book-list")
def book_list_page(
    db: Session = Depends(get_db),
    email: str | None = Cookie(default=None),
    password: str | None = Cookie(default=None)
):
    user = authenticate_user(db, email, password)
    if user:
        output = render_book_list(db, email, password)
        return HTMLResponse(output)
    else:
        return RedirectResponse("/login")
    
def render_book_list(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if user.is_admin:
        book_list_page = env.get_template('book-list-roles/admin-book-list.html')
        output = book_list_page.render(
        books=db.query(Book).all(),
        username=email
    )
    else:
        book_list_page = env.get_template('book-list-roles/user-book-list.html')
        output = book_list_page.render(
        books=db.query(Book).all(),
        username=email,
        rents_book_id = [rent.books_id for rent in db.query(History).filter(
            History.user_id == user.id,
            History.isReturned == False
        ).all()] 
    )
    return output

@app.get("/book/{book_id}")
def book_page(book_id, db: Session = Depends(get_db)):
    book =  db.query(Book).filter(Book.id == book_id).first()     # якщо не знайдений, відправляємо статусний код і повідомлення про помилку
    if book==None:
        return JSONResponse(status_code=404, content={ "message": "Книжка не знайдена"})        #якщо користувача знайдено, відправляємо його
    return book

@app.post("/book")
def book_post_page(email: str| None = Cookie(default=None), password: str | None = Cookie(default=None), book_data = Body(), db: Session = Depends(get_db)):
    book = Book(
        nameBook=book_data.get("nameBook"),
        yearBook=book_data.get("yearBook"),
        availableBook=book_data.get("availableBook"),
        category_id=book_data.get("category_id"),
        author_id=book_data.get("author_id")
    )
    user = authenticate_user(db, email, password)
    if user.is_admin:
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed")
@app.put("/book")
def edit_book(email: str| None = Cookie(default=None), password: str | None = Cookie(default=None), data = Body(), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed")
    # отримуємо book за id
    book = db.query(Book).filter(Book.id == data["id"]).first()
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку
    if book == None:
        return JSONResponse(status_code=404, content={ "message": "Книжка не знайдена"})
    # якщо book знайдений, змінюємо його дані і відправляємо назад клієнту
    book.nameBook = data["nameBook"]
    book.yearBook = data["yearBook"]
    book.availableBook =  data["availableBook"]
    book.category_id =  data["category_id"]
    book.author_id =  data["author_id"]
    db.commit() # зберігаємо зміни
    db.refresh(book)
    return book

@app.delete("/book/{book_id}")
def delete_book(book_id, email: str| None = Cookie(default=None), password: str | None = Cookie(default=None),  db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed")
    # отримуємо користувача за id
    book = db.query(Book).filter(Book.id == book_id).first()
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку
    if book == None:
        return JSONResponse( status_code=404, content={ "message": "Книжка не знайдена"})
    # якщо користувача знайдено, видаляємо його
    db.delete(book) # видаляємо об'єкт
    db.commit() # зберігаємо зміни
    return book

@app.post("/book/{book_id}/rent")
def rent_book(
    book_id,
    email: str | None = Cookie(default=None),
    password: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    date = datetime.now()
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    # Update existing rental record
    rent = db.query(History).filter(
            History.user_id == user.id,
            History.isReturned == False,
            History.books_id == book_id
        ).first()
    book = db.query(Book).get(book_id)
    if rent:        #not returned rental rec
        rent.isReturned = True
        rent.dateReturn = date
        book.availableBook += 1
        db.commit() # зберігаємо зміни
        db.refresh(rent)
        db.refresh(book)
        return book
    else:       #creating a new rental rec
        # Create new rental record
        rent = History(user_id=user.id, books_id=book_id, dateLoan=date, isReturned=False)
        try:
            book.availableBook -= 1
            db.add(rent)
            db.commit()
            db.refresh(rent)
            db.refresh(book)
            return book
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/rents-list")
def book_list_page(
    db: Session = Depends(get_db),
    email: str | None = Cookie(default=None),
    password: str | None = Cookie(default=None)
):
    user = authenticate_user(db, email, password)
    if user:
        output = render_rent_list(db, email, password)
        return HTMLResponse(output)
    else:
        return RedirectResponse("/login")

def render_rent_list(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if user.is_admin:
        book_list_page = env.get_template('rent-list.html')
        output = book_list_page.render(
        rents = db.query(History).order_by(History.isReturned.asc(), History.dateLoan.desc()).all(),
        username=email
    )
    else:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed")
    return output

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
def books_post_page(data: dict = Body(...), db: Session = Depends(get_db)):
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

@app.get("/clear-cookie")
def clear_cookie(response: Response):
    response.delete_cookie("email")
    response.delete_cookie("password")
    return {"message": "Cookie cleared successfully"}
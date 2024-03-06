from sqlalchemy.orm import sessionmaker
from models import *
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()
# db = SessionLocal()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return FileResponse("public/index.html")
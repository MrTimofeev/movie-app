from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, crud, schemas, scraper
from .database import SessionLocal, engine
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Подключаем папку static как источник статических файлов
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
# Подключаем папку images как статическую
app.mount("/backend/images",
          StaticFiles(directory="backend/images"), name="images")

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    file_path = os.path.abspath(os.path.join("frontend", "index.html"))
    with open(file_path) as f:
        return HTMLResponse(content=f.read())


@app.get("/movies", response_model=list[schemas.Movie])
def read_movies(db: Session = Depends(get_db)):
    return crud.get_all_movies(db)


@app.post("/movies/load")
def load_movies(db: Session = Depends(get_db)):
    movies = scraper.scrape_movies()
    for movie in movies:
        crud.create_movie(db, schemas.MovieCreate(**movie))
    return {"status": "success"}

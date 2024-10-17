from sqlalchemy.orm import Session
from . import models, schemas


def get_all_movies(db: Session):
    return db.query(models.Movie).order_by(models.Movie.rating_IMDb.desc()).all()


def create_movie(db: Session, movie: schemas.MovieCreate):
    # Проверяем, существует ли уже фильм с таким названием
    existing_movie = db.query(models.Movie).filter(
        models.Movie.title == movie.title).first()

    if existing_movie:
        # Если фильм уже существует, ничего не делаем
        return existing_movie

    # Если фильм не найден, создаем новый
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

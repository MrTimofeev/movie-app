from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    rating = Column(Float)
    rating_IMDb = Column(Float)
    genre = Column(String)
    director = Column(String)
    image_path = Column(String)

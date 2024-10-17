from pydantic import BaseModel
from typing import ClassVar


class MovieBase(BaseModel):
    title: str
    description: str
    rating: float
    rating_IMDb: float
    genre: str
    director: str
    image_path: str


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int

    ConfigDict: ClassVar[dict] = {
        "from_attributes": True  
    }

import datetime

from pydantic import BaseModel, ConfigDict


class MovieBaseSchema(BaseModel):
    name: str
    date: datetime.date
    score: float
    overview: str

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieBaseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int


# class MovieDetailSchema
#     pass


# class MovieListItemSchema
#     pass

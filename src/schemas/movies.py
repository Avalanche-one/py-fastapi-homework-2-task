import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CountryResponseSchema(BaseModel):
    id: int
    code: str
    name: str | None

    model_config = ConfigDict(from_attributes=True)


class RelatedEntitySchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class MovieStatus(str, Enum):
    RELEASED = "Released"
    POST_PRODUCTION = "Post Production"
    IN_PRODUCTION = "In Production"


class MovieBaseSchema(BaseModel):
    name: str
    date: datetime.date
    score: float
    overview: str


class MovieListItemSchema(MovieBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieListItemSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int


class MovieCreateSchema(MovieBaseSchema):
    name: str = Field(max_length=255)
    score: float = Field(ge=0, le=100)
    status: MovieStatus
    budget: float = Field(ge=0)
    revenue: float = Field(ge=0)
    country: str = Field(
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$"
    )
    genres: list[str]
    actors: list[str]
    languages: list[str]

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: datetime.date) -> datetime.date:
        today = datetime.date.today()

        try:
            max_date = today.replace(year=today.year + 1)
        except ValueError:
            max_date = today.replace(
                year=today.year + 1,
                day=28
            )

        if value > max_date:
            raise ValueError(
                "Release date cannot be more than one year in the future."
            )

        return value


class MovieCreateResponseSchema(MovieListItemSchema):
    status: str
    budget: float
    revenue: float
    country: CountryResponseSchema
    genres: list[RelatedEntitySchema]
    actors: list[RelatedEntitySchema]
    languages: list[RelatedEntitySchema]

    model_config = ConfigDict(from_attributes=True)


# class MovieDetailSchema
#     pass


# class MovieListItemSchema
#     pass

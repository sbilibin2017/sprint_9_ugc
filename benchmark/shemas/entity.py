import datetime
import random
import typing
import uuid
from enum import Enum
from typing import Union

import pydantic
from pydantic import Field, field_validator


class QueryTimeResult(pydantic.BaseModel):
    execute_time: float
    execute_result: typing.Any


class LikeType(Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class Bookmark(pydantic.BaseModel):
    pass


class Review(pydantic.BaseModel):
    text: str = "Отличное семейное кино!"


class Rating(pydantic.BaseModel):
    rating: int = Field(default_factory=lambda: random.randint(1, 10))

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v):
        if not (0 <= v <= 10):
            raise ValueError("Rating must be between 0 and 10")
        return v


class Like(pydantic.BaseModel):
    like_type: LikeType = Field(
        default_factory=lambda: random.choice(list(LikeType)).value
    )


class Event(pydantic.BaseModel):
    _id: uuid.UUID
    user_id: uuid.UUID
    movie_id: uuid.UUID
    event_type: str
    event_data: Bookmark | Rating | Review | Like
    created_at: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )
    updated_at: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )

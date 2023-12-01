import datetime
import uuid

import libs.actions.models as actions_models
import libs.actions.utils as actions_utils
import pydantic


class ReviewCreatePayloadModel(pydantic.BaseModel):
    text: str


class ReviewCreateRequestModel(pydantic.BaseModel):
    timestamp: int
    payload: ReviewCreatePayloadModel


class ReviewResponseModel(actions_models.ReviewBaseModel):
    id: actions_utils.CustomObjectId = pydantic.Field(default=..., alias="_id")
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

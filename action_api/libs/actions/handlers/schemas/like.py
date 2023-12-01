import datetime
import uuid

import libs.actions.models as actions_models
import libs.actions.utils as actions_utils
import pydantic


class LikeCreatePayloadModel(pydantic.BaseModel):
    item_type: str
    rating: int = pydantic.Field(default=..., ge=0, le=10)  # value "0" - unrated

    @pydantic.field_validator("item_type")
    def validate_item_type(cls, value: str) -> str:
        if value not in ("movie", "review"):
            raise ValueError("item_type must be either 'movie' or 'review'")
        return value


class LikeCreateRequestModel(pydantic.BaseModel):
    timestamp: int
    payload: LikeCreatePayloadModel


class LikeResponseModel(actions_models.LikeBaseModel):
    id: actions_utils.CustomObjectId = pydantic.Field(default=..., alias="_id")
    user_id: uuid.UUID
    item_id: uuid.UUID
    item_type: actions_utils.ItemTypeEnum
    rating: int = pydantic.Field(default=..., ge=0, le=10)  # value "0" - unrated
    created_at: datetime.datetime
    updated_at: datetime.datetime


class LikeRatingPayloadModel(pydantic.BaseModel):
    item_type: actions_utils.ItemTypeEnum

    @pydantic.field_validator("item_type")
    def validate_item_type(cls, value: str) -> str:
        if value not in ("movie", "review"):
            raise ValueError("item_type must be either 'movie' or 'review'")
        return value


class LikeRatingRequestModel(pydantic.BaseModel):
    timestamp: int
    payload: LikeRatingPayloadModel


class LikeRatingResponseModel(pydantic.BaseModel):
    rating: int | float = pydantic.Field(default=..., ge=0)

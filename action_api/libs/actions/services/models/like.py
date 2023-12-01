import datetime
import typing
import uuid

import libs.actions.models as actions_models
import libs.actions.models.mixins as actions_services_models_mixins
import libs.actions.utils as actions_utils
import pydantic


class LikeCreateModel(
    actions_services_models_mixins.NoIdDateMixin, actions_models.LikeBaseModel
):
    ...


class LikeFullResponseModel(actions_models.LikeBaseModel):
    id: actions_utils.CustomObjectId = pydantic.Field(default=..., alias="_id")
    user_id: uuid.UUID
    item_id: uuid.UUID
    item_type: actions_utils.ItemTypeEnum
    rating: int = pydantic.Field(default=..., ge=0, le=10)  # value "0" - unrated
    created_at: datetime.datetime
    updated_at: datetime.datetime


class LikeSearchModel(actions_models.LikeBaseModel):
    @pydantic.model_validator(mode="before")
    def required_one(cls, values: dict[str, typing.Any]) -> dict[str, typing.Any]:
        if not any(values):
            raise ValueError(f"At least one of the fields must be provided")
        return values


class LikeRatingRequest(pydantic.BaseModel):
    item_id: uuid.UUID
    item_type: actions_utils.ItemTypeEnum


class LikeRatingResponse(
    actions_services_models_mixins.NoIdDateMixin, actions_models.LikeBaseModel
):
    rating: int = pydantic.Field(default=..., ge=0, le=10)  # value "0" - unrated

    user_id: None = pydantic.Field(default=None, exclude=True)
    item_id: None = pydantic.Field(default=None, exclude=True)
    item_type: None = pydantic.Field(default=None, exclude=True)


class LikeRatingListResponse(pydantic.BaseModel):
    response: list[LikeRatingResponse]

    def get_rating_likes_count(self) -> int:
        """For likes and dislikes"""
        return sum(map(lambda item: item.rating > 5, self.response))

    def get_average_rating(self) -> float:
        response_sum = sum(map(lambda item: item.rating, self.response))
        response_len = len(
            tuple(
                filter(
                    lambda item: item.rating != 0, self.response  # type: ignore[reportUnknownLambdaType]
                )
            )
        )
        if response_len == 0:
            return 0
        return response_sum / response_len

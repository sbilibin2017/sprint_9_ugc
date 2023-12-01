import datetime
import typing
import uuid

import libs.actions.models as actions_models
import libs.actions.models.mixins as actions_services_models_mixins
import libs.actions.services.models.paginate as actions_services_models_paginate
import libs.actions.utils as actions_utils
import pydantic


class ReviewCreateModel(
    actions_services_models_mixins.NoIdDateMixin, actions_models.ReviewBaseModel
):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str


class ReviewFullResponseModel(actions_models.ReviewBaseModel):
    id: actions_utils.CustomObjectId = pydantic.Field(default=..., alias="_id")
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ReviewSearchModel(actions_models.ReviewBaseModel):
    @pydantic.model_validator(mode="before")
    def required_one(cls, values: dict[str, typing.Any]) -> dict[str, typing.Any]:
        if not any(values):
            raise ValueError(f"At least one of the fields must be provided")
        return values


class ReviewPaginateRequestModel(actions_services_models_paginate.PaginateRequestModel):
    search_data: ReviewSearchModel


class ReviewListPaginateModel(actions_services_models_paginate.PaginateResponseModel):
    items: list[ReviewFullResponseModel]

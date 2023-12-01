import datetime
import typing
import uuid

import libs.actions.models as actions_models
import libs.actions.utils as actions_utils
import pydantic


class CreateRequestBaseModel(
    actions_models.NoIdDateMixin,
    actions_models.LikeBaseModel,
    actions_models.ReviewBaseModel,
    actions_models.BookmarkBaseModel,
):
    @pydantic.model_validator(mode="before")
    def required_one(cls, values: dict[str, typing.Any]) -> dict[str, typing.Any]:
        if not any(values):
            raise ValueError(f"At least one of the fields must be provided")
        return values

    @pydantic.field_serializer("user_id", "item_id", "movie_id")
    def serialize_uuid(self, item_uuid: uuid.UUID | None) -> str | None:
        if not item_uuid:
            return item_uuid
        return item_uuid.hex


class SearchRequestBaseModel(
    actions_models.LikeBaseModel,
    actions_models.ReviewBaseModel,
    actions_models.BookmarkBaseModel,
):
    field_names: list[str] | None = pydantic.Field(default=None, exclude=True)

    @pydantic.model_validator(mode="before")
    def required_one(cls, values: dict[str, typing.Any]) -> dict[str, typing.Any]:
        if not any(filter(lambda item: item != "field_names", values)):
            raise ValueError(f"At least one of the fields must be provided")
        return values

    @pydantic.field_serializer("user_id", "item_id", "movie_id")
    def serialize_uuid(self, item_uuid: uuid.UUID | None) -> str | None:
        if not item_uuid:
            return item_uuid
        return item_uuid.hex


class FullResponseBaseModel(
    actions_models.LikeBaseModel,
    actions_models.ReviewBaseModel,
    actions_models.BookmarkBaseModel,
):
    id: actions_utils.CustomObjectId | None = pydantic.Field(None, alias="_id")
    user_id: uuid.UUID | None = None
    created_at: datetime.datetime | None = None

    @pydantic.field_serializer("user_id", "item_id", "movie_id")
    def serialize_uuid(self, item_uuid: uuid.UUID | None) -> str | None:
        if not item_uuid:
            return item_uuid
        return item_uuid.hex


class ListFullResponseBaseModel(pydantic.BaseModel):
    response: list[FullResponseBaseModel]


class PaginateRequestBaseModel(actions_models.PaginateRequestMixin):
    search_data: SearchRequestBaseModel


class PaginateResponseBaseModel(actions_models.PaginateResponseMixin):
    prev: None = pydantic.Field(default=None, exclude=True)
    next: None = pydantic.Field(default=None, exclude=True)
    items: list[FullResponseBaseModel]

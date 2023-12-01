import datetime
import uuid

import libs.actions.utils as actions_utils
import pydantic


class LikeBaseModel(pydantic.BaseModel):
    id: actions_utils.CustomObjectId | None = pydantic.Field(default=None, alias="_id")
    user_id: uuid.UUID | None = None
    item_id: uuid.UUID | None = None
    item_type: actions_utils.ItemTypeEnum | None = None
    rating: int | None = pydantic.Field(
        default=None, ge=0, le=10
    )  # value "0" - unrated
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    @pydantic.field_validator("item_type")
    def validate_item_type(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if value not in ("movie", "review"):
            raise ValueError("item_type must be either 'movie' or 'review'")
        return value

    @pydantic.field_serializer("user_id", "item_id")
    def serialize_uuid(self, item_uuid: uuid.UUID | None) -> str | None:
        if not item_uuid:
            return item_uuid
        return item_uuid.hex

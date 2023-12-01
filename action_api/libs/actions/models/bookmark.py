import datetime
import uuid

import libs.actions.utils as actions_utils
import pydantic


class BookmarkBaseModel(pydantic.BaseModel):
    id: actions_utils.CustomObjectId | None = pydantic.Field(default=None, alias="_id")
    user_id: uuid.UUID | None = None
    movie_id: uuid.UUID | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    @pydantic.field_serializer("user_id", "movie_id")
    def serialize_uuid(self, item_uuid: uuid.UUID | None) -> str | None:
        if not item_uuid:
            return item_uuid
        return item_uuid.hex

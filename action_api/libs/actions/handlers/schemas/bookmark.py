import datetime
import uuid

import libs.actions.models as actions_models
import libs.actions.utils as actions_utils
import pydantic


class BookmarkResponseModel(actions_models.BookmarkBaseModel):
    id: actions_utils.CustomObjectId = pydantic.Field(default=..., alias="_id")
    user_id: uuid.UUID
    movie_id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

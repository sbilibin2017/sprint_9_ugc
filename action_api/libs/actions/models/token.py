import uuid

import pydantic


class TokenResponseModel(pydantic.BaseModel):
    sub: uuid.UUID
    exp: int | None = None

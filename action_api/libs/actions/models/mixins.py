import pydantic


class NoIdDateMixin(pydantic.BaseModel):
    id: None = pydantic.Field(default=None, alias="_id", exclude=True)
    created_at: None = pydantic.Field(default=None, exclude=True)
    updated_at: None = pydantic.Field(default=None, exclude=True)


class PaginateRequestMixin(pydantic.BaseModel):
    page_number: int = pydantic.Field(default=1, ge=1)
    page_size: int = pydantic.Field(default=20, ge=1)


class PaginateResponseMixin(pydantic.BaseModel):
    prev: int | None = None
    next: int | None = None
    pages_total: int = 0

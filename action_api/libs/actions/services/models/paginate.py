import typing

import libs.actions.models.mixins as actions_services_models_mixins
import pydantic


class PaginateRequestModel(actions_services_models_mixins.PaginateRequestMixin):
    ...


class PaginateResponseModel(actions_services_models_mixins.PaginateResponseMixin):
    model_config = {"extra": "ignore"}

    def __init__(self, **data: typing.Any):
        page_number = data.get("page_number")
        pages_total = data.get("pages_total")
        if (
            page_number
            and pages_total
            and isinstance(page_number, int)
            and isinstance(pages_total, int)
        ):
            data["prev"] = page_number - 1 if page_number > 1 else None
            data["next"] = page_number + 1 if page_number < pages_total else None

        super().__init__(**data)

    @pydantic.model_validator(mode="before")
    def required_one(cls, values: dict[str, typing.Any]) -> dict[str, typing.Any]:
        if (values.get("prev") or values.get("next")) or values.get("page_number"):
            return values
        raise ValueError(
            f"At least one of the fields (prev or next) or (page_number) must be provided"
        )

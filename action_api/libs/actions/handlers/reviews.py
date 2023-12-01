import http
import typing
import uuid

import fastapi
import libs.actions.handlers.schemas as actions_handlers_schemas
import libs.actions.models as actions_models
import libs.actions.services as actions_services

router = fastapi.APIRouter()


@router.post(
    "/{movie_id}",
    description="Добавляет рецензию пользователя к фильму",
    response_description="Возвращает информацию о добавленной рецензии",
    response_model=actions_handlers_schemas.ReviewResponseModel,
    status_code=http.HTTPStatus.CREATED,
)
async def review_add(
    movie_id: uuid.UUID,
    data: actions_handlers_schemas.ReviewCreateRequestModel,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    review_service: actions_services.ReviewService = fastapi.Depends(
        actions_services.get_review_service
    ),
) -> actions_handlers_schemas.ReviewResponseModel:
    user_id = token_data.sub
    review_data_dict = {
        "user_id": user_id,
        "movie_id": movie_id,
        **data.model_dump()["payload"],
    }
    review_data_create = actions_services.ReviewCreateModel.model_validate(
        review_data_dict
    )
    response = await review_service.create_one(review_data_create)
    response_validated = actions_handlers_schemas.ReviewResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated


@router.delete(
    "/{movie_id}",
    description="Удаляет рецензию пользователя к фильму",
    response_description="Возвращает информацию об удаленной рецензии",
    response_model=actions_handlers_schemas.ReviewResponseModel,
    status_code=http.HTTPStatus.OK,
)
async def review_remove(
    movie_id: uuid.UUID,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    review_service: actions_services.ReviewService = fastapi.Depends(
        actions_services.get_review_service
    ),
) -> actions_handlers_schemas.ReviewResponseModel:
    user_id = token_data.sub
    review_data_dict = {
        "user_id": user_id,
        "movie_id": movie_id,
    }
    review_data_search = actions_services.ReviewSearchModel.model_validate(
        review_data_dict
    )
    response = await review_service.delete_one(review_data_search)
    if response is None:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND, detail="Item not found"
        )

    response_validated = actions_handlers_schemas.ReviewResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated


@router.get(
    "/{movie_id}",
    description="Получает рецензию пользователя к фильму",
    response_description="Возвращает информацию о рецензии",
    response_model=actions_handlers_schemas.ReviewResponseModel,
    status_code=http.HTTPStatus.OK,
)
async def review_get(
    movie_id: uuid.UUID,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    review_service: actions_services.ReviewService = fastapi.Depends(
        actions_services.get_review_service
    ),
) -> actions_handlers_schemas.ReviewResponseModel:
    user_id = token_data.sub
    review_data_dict = {
        "user_id": user_id,
        "movie_id": movie_id,
    }
    review_data_search = actions_services.ReviewSearchModel.model_validate(
        review_data_dict
    )
    response = await review_service.get_one(review_data_search)
    if response is None:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND, detail="Item not found"
        )

    response_validated = actions_handlers_schemas.ReviewResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated

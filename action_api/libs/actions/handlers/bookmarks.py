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
    description="Добавляет фильм в закладки пользователя",
    response_description="Возвращает информацию о добавленной закладке",
    response_model=actions_handlers_schemas.BookmarkResponseModel,
    status_code=http.HTTPStatus.CREATED,
)
async def bookmark_add(
    movie_id: uuid.UUID,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    bookmark_service: actions_services.BookmarkService = fastapi.Depends(
        actions_services.get_bookmark_service
    ),
) -> actions_handlers_schemas.BookmarkResponseModel:
    user_id = token_data.sub
    bookmark_data_dict = {
        "user_id": user_id,
        "movie_id": movie_id,
    }
    bookmark_data_create = actions_services.BookmarkCreateModel.model_validate(
        bookmark_data_dict
    )
    response = await bookmark_service.create_one(bookmark_data_create)
    response_validated = actions_handlers_schemas.BookmarkResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated


@router.delete(
    "/{movie_id}",
    description="Удаляет закладку пользователя к фильму",
    response_description="Возвращает информацию об удаленной закладке",
    response_model=actions_handlers_schemas.BookmarkResponseModel,
    status_code=http.HTTPStatus.OK,
)
async def bookmark_remove(
    movie_id: uuid.UUID,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    bookmark_service: actions_services.BookmarkService = fastapi.Depends(
        actions_services.get_bookmark_service
    ),
) -> actions_handlers_schemas.BookmarkResponseModel:
    user_id = token_data.sub
    bookmark_data_dict = {
        "user_id": user_id,
        "movie_id": movie_id,
    }
    bookmark_data_search = actions_services.BookmarkSearchModel.model_validate(
        bookmark_data_dict
    )
    response = await bookmark_service.delete_one(bookmark_data_search)
    if response is None:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND, detail="Item not found"
        )

    response_validated = actions_handlers_schemas.BookmarkResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated


@router.get(
    "/{movie_id}",
    description="Получает закладку пользователя к фильму",
    response_description="Возвращает информацию о закладке",
    response_model=actions_handlers_schemas.BookmarkResponseModel,
    status_code=http.HTTPStatus.OK,
)
async def bookmark_get(
    movie_id: uuid.UUID,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    bookmark_service: actions_services.BookmarkService = fastapi.Depends(
        actions_services.get_bookmark_service
    ),
) -> actions_handlers_schemas.BookmarkResponseModel:
    user_id = token_data.sub
    bookmark_data_dict = {
        "user_id": user_id,
        "movie_id": movie_id,
    }
    bookmark_data_search = actions_services.BookmarkSearchModel.model_validate(
        bookmark_data_dict
    )
    response = await bookmark_service.get_one(bookmark_data_search)
    if response is None:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND, detail="Item not found"
        )

    response_validated = actions_handlers_schemas.BookmarkResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated

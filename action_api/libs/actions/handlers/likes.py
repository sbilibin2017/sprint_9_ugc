import http
import typing
import uuid

import fastapi
import libs.actions.handlers.schemas as actions_handlers_schemas
import libs.actions.models as actions_models
import libs.actions.services as actions_services

router = fastapi.APIRouter()


@router.post(
    "/{item_id}",
    description="Добавляет оценку пользователя к объекту",
    response_description="Возвращает информацию об объекте, который был оценен",
    response_model=actions_handlers_schemas.LikeResponseModel,
    status_code=http.HTTPStatus.CREATED,
)
async def like_add(
    item_id: uuid.UUID,
    data: actions_handlers_schemas.LikeCreateRequestModel,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    like_service: actions_services.LikeService = fastapi.Depends(
        actions_services.get_like_service
    ),
) -> actions_handlers_schemas.LikeResponseModel:
    user_id = token_data.sub
    like_data_dict = {
        "user_id": user_id,
        "item_id": item_id,
        **data.model_dump()["payload"],
    }
    like_data_create = actions_services.LikeCreateModel.model_validate(like_data_dict)
    response = await like_service.create_one(like_data_create)
    response_validated = actions_handlers_schemas.LikeResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated


@router.delete(
    "/{item_id}",
    description="Удаляет оценку пользователя к объекту",
    response_description="Возвращает информацию об объекте, который был оценен",
    response_model=actions_handlers_schemas.LikeResponseModel,
    status_code=http.HTTPStatus.OK,
)
async def like_remove(
    item_id: uuid.UUID,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    like_service: actions_services.LikeService = fastapi.Depends(
        actions_services.get_like_service
    ),
) -> actions_handlers_schemas.LikeResponseModel:
    user_id = token_data.sub
    like_data_dict = {
        "user_id": user_id,
        "item_id": item_id,
    }
    like_data_search = actions_services.LikeSearchModel.model_validate(like_data_dict)
    response = await like_service.delete_one(like_data_search)
    if response is None:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND, detail="Item not found"
        )

    response_validated = actions_handlers_schemas.LikeResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated


@router.get(
    "/{item_id}",
    description="Получает оценку пользователя к объекту",
    response_description="Возвращает информацию об объекте, который был оценен",
    response_model=actions_handlers_schemas.LikeResponseModel,
    status_code=http.HTTPStatus.OK,
)
async def like_get(
    item_id: uuid.UUID,
    token_data: typing.Annotated[
        actions_models.TokenResponseModel,
        fastapi.Depends(actions_services.get_token_data),
    ],
    like_service: actions_services.LikeService = fastapi.Depends(
        actions_services.get_like_service
    ),
) -> actions_handlers_schemas.LikeResponseModel:
    user_id = token_data.sub
    like_data_dict = {
        "user_id": user_id,
        "item_id": item_id,
    }
    like_data_search = actions_services.LikeSearchModel.model_validate(like_data_dict)
    response = await like_service.get_one(like_data_search)
    if response is None:
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.NOT_FOUND, detail="Item not found"
        )

    response_validated = actions_handlers_schemas.LikeResponseModel.model_validate(
        response.model_dump(by_alias=True)
    )
    return response_validated


@router.get(
    "/{item_id}/rating",
    description="Получает оценку всех пользователей к объекту."
    "К фильму — среднеарифметическое, к рецензии — количество лайков",
    response_description="Возвращает информацию об объекте, который был оценен",
    response_model=actions_handlers_schemas.LikeRatingResponseModel,
    status_code=http.HTTPStatus.OK,
)
async def like_get_rating(
    item_id: uuid.UUID,
    data: actions_handlers_schemas.LikeRatingRequestModel,
    like_service: actions_services.LikeService = fastapi.Depends(
        actions_services.get_like_service
    ),
) -> actions_handlers_schemas.LikeRatingResponseModel:
    data_payload = data.model_dump()["payload"]
    like_data_search = actions_services.LikeRatingRequest.model_validate(
        {"item_id": item_id, "item_type": data_payload["item_type"]}
    )
    response = await like_service.get_item_rating(like_data_search)

    response_validated = (
        actions_handlers_schemas.LikeRatingResponseModel.model_validate(
            {"rating": response}
        )
    )
    return response_validated

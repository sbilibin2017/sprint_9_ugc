import http
import typing
import uuid

import pytest
import tests.functional.models as tests_models
import tests.functional.testdata as testdata
from tests.functional.fixtures import *

pytestmark = [pytest.mark.asyncio]


@pytest.mark.parametrize(
    "create_body,item_id,jwt_token",
    testdata.LIKE_GET_DATA,
)
async def test_like_get(
    create_body: dict[str, typing.Any],
    item_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    await make_request(
        api_method=f"likes/{item_id}",
        method="post",
        body=create_body,
        jwt_token=jwt_token,
    )
    response = await make_request(
        method="get", api_method=f"likes/{item_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.OK


@pytest.mark.parametrize(
    "item_id,jwt_token",
    testdata.LIKE_GET_NO_DATA,
)
async def test_like_get_no_data(
    item_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        method="get", api_method=f"likes/{item_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "create_body,item_id,jwt_token",
    testdata.LIKE_GET_INVALID,
)
async def test_like_get_invalid(
    create_body: dict[str, typing.Any],
    item_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    await make_request(
        api_method=f"likes/{item_id}",
        method="post",
        body=create_body,
        jwt_token=jwt_token,
    )
    response = await make_request(
        method="get", api_method=f"likes/{item_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "create_bodies,get_body,rating_expected,item_id,jwt_token",
    testdata.LIKE_GET_RATING_DATA,
)
async def test_like_get_rating(
    create_bodies: list[dict[str, typing.Any]],
    get_body: dict[str, typing.Any],
    rating_expected: int,
    item_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    for create_body in create_bodies:
        body_dict = create_body.copy()
        jwt_token_ = body_dict.pop("jwt_token")
        await make_request(
            api_method=f"likes/{item_id}",
            method="post",
            body=create_body,
            jwt_token=jwt_token_,
        )
    response = await make_request(
        method="get",
        api_method=f"likes/{item_id}/rating",
        body=get_body,
        jwt_token=jwt_token,
    )
    assert response.status_code == http.HTTPStatus.OK


@pytest.mark.parametrize(
    "get_body,rating_expected,item_id,jwt_token",
    testdata.LIKE_GET_RATING_INVALID,
)
async def test_like_get_rating_invalid(
    get_body: dict[str, typing.Any],
    rating_expected: int,
    item_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        method="get",
        api_method=f"likes/{item_id}/rating",
        body=get_body,
        jwt_token=jwt_token,
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY

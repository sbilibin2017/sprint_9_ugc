import http
import typing
import uuid

import pytest
import tests.functional.models as tests_models
import tests.functional.testdata as testdata
from tests.functional.fixtures import *

pytestmark = [pytest.mark.asyncio]


@pytest.mark.parametrize(
    "body,item_id,jwt_token",
    testdata.LIKE_ADD_DATA,
)
async def test_like_add(
    body: dict[str, typing.Any],
    item_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        api_method=f"likes/{item_id}", method="post", body=body, jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.CREATED


@pytest.mark.parametrize(
    "body,item_id,jwt_token",
    testdata.LIKE_ADD_INVALID_BODY,
)
async def test_like_add_invalid_body(
    body: dict[str, typing.Any],
    item_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        api_method=f"likes/{item_id}", method="post", body=body, jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "body,item_id,jwt_token,error",
    testdata.LIKE_INVALID_TOKEN,
)
async def test_like_add_invalid_token(
    body: dict[str, typing.Any],
    item_id: uuid.UUID,
    jwt_token: str,
    error: http.HTTPStatus,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        api_method=f"likes/{item_id}", method="post", body=body, jwt_token=jwt_token
    )
    assert response.status_code == error

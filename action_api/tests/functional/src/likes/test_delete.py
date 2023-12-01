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
    testdata.LIKE_DELETE_DATA,
)
async def test_like_delete(
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
        method="delete", api_method=f"likes/{item_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.OK


@pytest.mark.parametrize(
    "item_id,jwt_token",
    testdata.LIKE_DELETE_NO_DATA,
)
async def test_like_delete_no_data(
    item_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        method="delete", api_method=f"likes/{item_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "create_body,item_id,jwt_token",
    testdata.LIKE_DELETE_INVALID,
)
async def test_like_delete_invalid(
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
        method="delete", api_method=f"likes/{item_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY

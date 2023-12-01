import http
import typing
import uuid

import pytest
import tests.functional.models as tests_models
import tests.functional.testdata as testdata
from tests.functional.fixtures import *

pytestmark = [pytest.mark.asyncio]


@pytest.mark.parametrize(
    "create_body,movie_id,jwt_token",
    testdata.REVIEW_GET_DATA,
)
async def test_review_get(
    create_body: dict[str, typing.Any],
    movie_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    await make_request(
        method="post",
        api_method=f"reviews/{movie_id}",
        body=create_body,
        jwt_token=jwt_token,
    )
    response = await make_request(
        method="get", api_method=f"reviews/{movie_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.OK


@pytest.mark.parametrize(
    "movie_id,jwt_token",
    testdata.REVIEW_GET_NO_DATA,
)
async def test_review_get_no_data(
    movie_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        method="get", api_method=f"reviews/{movie_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "create_body,movie_id,jwt_token",
    testdata.REVIEW_GET_INVALID,
)
async def test_review_get_invalid(
    create_body: dict[str, typing.Any],
    movie_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    await make_request(
        method="post",
        api_method=f"reviews/{movie_id}",
        body=create_body,
        jwt_token=jwt_token,
    )
    response = await make_request(
        method="get", api_method=f"reviews/{movie_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY

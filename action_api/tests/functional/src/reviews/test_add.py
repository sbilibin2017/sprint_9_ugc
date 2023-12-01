import http
import typing
import uuid

import pytest
import tests.functional.models as tests_models
import tests.functional.testdata as testdata
from tests.functional.fixtures import *

pytestmark = [pytest.mark.asyncio]


@pytest.mark.parametrize(
    "body,movie_id,jwt_token",
    testdata.REVIEW_ADD_DATA,
)
async def test_review_add(
    body: dict[str, typing.Any],
    movie_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        api_method=f"reviews/{movie_id}", method="post", body=body, jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.CREATED


@pytest.mark.parametrize(
    "body,movie_id,jwt_token",
    testdata.REVIEW_ADD_INVALID,
)
async def test_review_invalid(
    body: dict[str, typing.Any],
    movie_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        method="post", api_method=f"reviews/{movie_id}", body=body, jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY

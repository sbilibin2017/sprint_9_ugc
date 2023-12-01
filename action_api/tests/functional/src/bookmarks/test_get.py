import http
import uuid

import pytest
import tests.functional.models as tests_models
import tests.functional.testdata as testdata
from tests.functional.fixtures import *

pytestmark = [pytest.mark.asyncio]


@pytest.mark.parametrize(
    "movie_id,jwt_token",
    testdata.BOOKMARK_GET_DATA,
)
async def test_bookmark_get(
    movie_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    await make_request(
        method="post",
        api_method=f"bookmarks/{movie_id}",
        jwt_token=jwt_token,
    )
    response = await make_request(
        method="get", api_method=f"bookmarks/{movie_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.OK


@pytest.mark.parametrize(
    "movie_id,jwt_token",
    testdata.BOOKMARK_GET_NO_DATA,
)
async def test_bookmark_get_no_data(
    movie_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    response = await make_request(
        method="get", api_method=f"bookmarks/{movie_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "movie_id,jwt_token",
    testdata.BOOKMARK_GET_INVALID,
)
async def test_bookmark_get_invalid(
    movie_id: uuid.UUID,
    jwt_token: str,
    make_request: tests_models.MakeResponseCallableType,
):
    await make_request(
        method="post",
        api_method=f"bookmarks/{movie_id}",
        jwt_token=jwt_token,
    )
    response = await make_request(
        method="get", api_method=f"bookmarks/{movie_id}", jwt_token=jwt_token
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY

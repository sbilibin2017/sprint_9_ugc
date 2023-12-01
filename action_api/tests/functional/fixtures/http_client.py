import typing

import aiohttp
import pytest_asyncio
import tests.config as config
import tests.functional.models as functional_models


@pytest_asyncio.fixture
async def http_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
async def make_request(http_client: aiohttp.ClientSession):
    async def inner(
        api_method: str = "",
        url: str = config.tests_settings.get_api_url(),
        method: typing.Literal["get", "post", "delete"] = "get",
        body: dict[str, typing.Any] | None = None,
        jwt_token: str | None = None,
    ) -> functional_models.HTTPResponse:
        if body is None:
            body = {}
        if api_method:
            url += api_method
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt_token}",
        }
        async with getattr(http_client, method)(
            url, json=body, headers=headers
        ) as response:
            return functional_models.HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status_code=response.status,
            )

    return inner

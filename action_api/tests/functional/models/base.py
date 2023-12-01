import dataclasses
import typing

import multidict


@dataclasses.dataclass
class HTTPResponse:
    body: dict[str, typing.Any] | str
    headers: multidict.CIMultiDictProxy[str]
    status_code: int


class MakeResponseCallableType(typing.Protocol):
    async def __call__(
        self,
        jwt_token: str,
        method: typing.Literal["get", "post", "delete"] = "get",
        api_method: str = "",
        body: dict[str, typing.Any] | None = None,
    ) -> HTTPResponse:
        ...

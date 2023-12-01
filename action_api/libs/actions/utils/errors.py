import typing


class RepositoryError(Exception):
    def __init__(self, message: str, *args: typing.Any) -> None:
        super().__init__(*args)
        self.message = message


class RepositoryOperationError(RepositoryError):
    pass

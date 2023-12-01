import abc
import logging
import typing

import libs.actions.repositories as actions_repositories
import motor.core as motor_core
import pydantic

logger = logging.getLogger(__name__)


class BaseService(abc.ABC):
    MODEL = typing.TypeVar("MODEL", bound=pydantic.BaseModel)

    def __init__(self, database: motor_core.AgnosticDatabase):
        self.database = database

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    def collection(self) -> actions_repositories.MongoCollectionService:
        return actions_repositories.MongoCollectionService(self.database[self.name])  # type: ignore[reportUnknownVariableType]

    @abc.abstractmethod
    async def create_one(
        self,
        create_data: type[MODEL],
    ) -> MODEL:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_one(
        self,
        search_data: type[MODEL],
    ) -> MODEL | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_one(
        self,
        search_data: type[MODEL],
    ) -> MODEL | None:
        raise NotImplementedError

    @classmethod
    def validate(
        cls, data: dict[typing.Any, typing.Any], validation_model: type[MODEL]
    ) -> MODEL:
        logger.debug("validate starts")
        try:
            entity_validated = validation_model.model_validate(data)
        except pydantic.ValidationError as e:
            logger.error("validate error", exc_info=True)
            raise e
        logger.debug("validate successful")
        return entity_validated

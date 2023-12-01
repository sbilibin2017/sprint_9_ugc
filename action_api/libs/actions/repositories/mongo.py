import abc
import datetime
import logging
import math
import typing

import libs.actions.repositories.models as actions_repositories_models
import libs.actions.utils.errors as app_errors
import motor.core as motor_core
import pymongo
import pymongo.errors as pymongo_errors

logger = logging.getLogger(__name__)


class MongoCollectionBaseService(abc.ABC):
    def __init__(
        self,
        collection: motor_core.AgnosticCollection,
    ) -> None:
        self.collection = collection

    @abc.abstractmethod
    async def get_one(
        self,
        search_data: actions_repositories_models.SearchRequestBaseModel,
    ) -> actions_repositories_models.FullResponseBaseModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_or_update_one(
        self,
        search_data: actions_repositories_models.SearchRequestBaseModel,
        create_data: actions_repositories_models.CreateRequestBaseModel,
    ) -> actions_repositories_models.FullResponseBaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_and_delete_one(
        self,
        search_data: actions_repositories_models.SearchRequestBaseModel,
    ) -> actions_repositories_models.FullResponseBaseModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_batch(
        self,
        paginate_data: actions_repositories_models.PaginateRequestBaseModel,
    ) -> actions_repositories_models.PaginateResponseBaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(
        self,
        search_data: actions_repositories_models.SearchRequestBaseModel,
    ) -> actions_repositories_models.ListFullResponseBaseModel:
        raise NotImplementedError


class MongoCollectionService(MongoCollectionBaseService):
    async def get_one(
        self,
        search_data: actions_repositories_models.SearchRequestBaseModel,
    ) -> actions_repositories_models.FullResponseBaseModel | None:
        try:
            response = await self.collection.find_one(  # type: ignore[reportGeneralTypeIssues]
                search_data.model_dump(exclude_none=True)
            )
        except pymongo_errors.OperationFailure as e:
            logger.error("get_one failed", exc_info=True)
            raise app_errors.RepositoryOperationError("get_one failed", e)

        if response is None:
            return None
        return actions_repositories_models.FullResponseBaseModel.model_validate(
            response
        )

    async def create_or_update_one(
        self,
        search_data: actions_repositories_models.SearchRequestBaseModel,
        create_data: actions_repositories_models.CreateRequestBaseModel,
    ) -> actions_repositories_models.FullResponseBaseModel:
        date_now = datetime.datetime.utcnow()
        try:
            response = await self.collection.find_one_and_update(  # type: ignore[reportGeneralTypeIssues]
                search_data.model_dump(exclude_none=True),
                {
                    "$set": {
                        "updated_at": date_now,
                        **create_data.model_dump(exclude_none=True),
                    },
                    "$setOnInsert": {"created_at": date_now},
                },
                upsert=True,
                return_document=pymongo.ReturnDocument.AFTER,
            )
        except pymongo_errors.OperationFailure as e:
            logger.error("create_or_update_one failed", exc_info=True)
            raise app_errors.RepositoryOperationError("create_or_update_one failed", e)

        return actions_repositories_models.FullResponseBaseModel.model_validate(
            response
        )

    async def get_and_delete_one(
        self,
        search_data: actions_repositories_models.SearchRequestBaseModel,
    ) -> actions_repositories_models.FullResponseBaseModel | None:
        try:
            response = await self.collection.find_one_and_delete(search_data.model_dump(exclude_none=True))  # type: ignore[reportGeneralTypeIssues, reportUnknownVariableType]
        except pymongo_errors.OperationFailure as e:
            logger.error("get_and_delete_one failed", exc_info=True)
            raise app_errors.RepositoryOperationError("get_and_delete_one failed", e)

        if response is None:
            return None
        return actions_repositories_models.FullResponseBaseModel.model_validate(
            response
        )

    @classmethod
    def __get_request_dict(
        cls, field_names: list[str] | None = None
    ) -> dict[str, bool]:
        if field_names is None:
            field_names = []
        field_names_dict = {field_name: True for field_name in field_names}
        if field_names_dict and "_id" not in field_names_dict:
            field_names_dict["_id"] = False
        return field_names_dict

    async def get_all(
        self,
        search_data: actions_repositories_models.SearchRequestBaseModel,
    ) -> actions_repositories_models.ListFullResponseBaseModel:
        field_names_dict = self.__get_request_dict(search_data.field_names)
        cursor: motor_core.AgnosticCursor = self.collection.find(  # type: ignore[reportUnknownVariableType]
            search_data.model_dump(exclude_none=True), field_names_dict
        )

        try:
            response: list[dict[typing.Any, typing.Any]] = await cursor.to_list(length=None)  # type: ignore[reportUnknownVariableType]
        except pymongo_errors.OperationFailure as e:
            logger.error("get_all to_list failed", exc_info=True)
            raise app_errors.RepositoryOperationError("get_all to_list failed", e)

        response_validated = (
            actions_repositories_models.ListFullResponseBaseModel.model_validate(
                {"response": response}
            )
        )
        return response_validated

    async def get_batch(
        self,
        paginate_data: actions_repositories_models.PaginateRequestBaseModel,
    ) -> actions_repositories_models.PaginateResponseBaseModel:
        field_names_dict = self.__get_request_dict(
            paginate_data.search_data.field_names
        )
        search_data_dict = paginate_data.search_data.model_dump(exclude_none=True)

        skip = (paginate_data.page_number - 1) * paginate_data.page_size

        try:
            items_count: int = await self.collection.count_documents(search_data_dict)  # type: ignore[reportUnknownVariableType]
        except pymongo_errors.OperationFailure as e:
            logger.error("get_batch count_documents failed", exc_info=True)
            raise app_errors.RepositoryOperationError(
                "get_batch count_documents failed", e
            )

        pages_total: int = math.ceil(items_count / paginate_data.page_size)  # type: ignore[reportUnknownVariableType]
        cursor: motor_core.AgnosticCursor = (  # type: ignore[reportUnknownVariableType]
            self.collection.find(search_data_dict, field_names_dict)  # type: ignore[reportGeneralTypeIssues]
            .skip(skip)
            .limit(paginate_data.page_size)
        )

        try:
            items: list[dict[typing.Any, typing.Any]] = await cursor.to_list(paginate_data.page_size)  # type: ignore[reportUnknownVariableType]
        except pymongo_errors.OperationFailure as e:
            logger.error("get_batch to_list failed", exc_info=True)
            raise app_errors.RepositoryOperationError("get_batch to_list failed", e)

        response = actions_repositories_models.PaginateResponseBaseModel.model_validate(
            {"pages_total": pages_total, "items": items}
        )

        return response

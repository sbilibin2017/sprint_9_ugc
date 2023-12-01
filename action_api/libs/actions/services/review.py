# pyright: reportIncompatibleMethodOverride=false


import functools

import fastapi
import libs.actions.repositories.models as actions_repositories_models
import libs.actions.services.base as actions_services_base
import libs.actions.services.models as actions_services_models
import libs.clients as clients
import motor.core as motor_core


class ReviewService(actions_services_base.BaseService):
    @property
    def name(self) -> str:
        return "review"

    async def create_one(
        self,
        create_data: actions_services_models.ReviewCreateModel,
    ) -> actions_services_models.ReviewFullResponseModel:
        create_data_dict = create_data.model_dump()
        create_data_validated = self.validate(
            create_data_dict, actions_repositories_models.CreateRequestBaseModel
        )
        search_data_validated = self.validate(
            create_data_dict, actions_repositories_models.SearchRequestBaseModel
        )

        response = await self.collection.create_or_update_one(
            search_data=search_data_validated,
            create_data=create_data_validated,
        )

        response_validated = self.validate(
            response.model_dump(by_alias=True),
            actions_services_models.ReviewFullResponseModel,
        )
        return response_validated

    async def get_one(
        self,
        search_data: actions_services_models.ReviewSearchModel,
    ) -> actions_services_models.ReviewFullResponseModel | None:
        search_data_validated = self.validate(
            search_data.model_dump(exclude_none=True, by_alias=True),
            actions_repositories_models.SearchRequestBaseModel,
        )
        response = await self.collection.get_one(search_data_validated)
        if response is None:
            return response

        response_validated = self.validate(
            response.model_dump(by_alias=True),
            actions_services_models.ReviewFullResponseModel,
        )
        return response_validated

    async def delete_one(
        self,
        search_data: actions_services_models.ReviewSearchModel,
    ) -> actions_services_models.ReviewFullResponseModel | None:
        search_data_validated = self.validate(
            search_data.model_dump(exclude_none=True, by_alias=True),
            actions_repositories_models.SearchRequestBaseModel,
        )
        response = await self.collection.get_and_delete_one(search_data_validated)
        if response is None:
            return response

        response_validated = self.validate(
            response.model_dump(by_alias=True),
            actions_services_models.ReviewFullResponseModel,
        )
        return response_validated

    async def get_page_data(
        self,
        paginate_data: actions_services_models.ReviewPaginateRequestModel,
    ) -> actions_services_models.ReviewListPaginateModel:
        paginate_data_dict = {
            **paginate_data.search_data.model_dump(exclude_none=True),
            **paginate_data.model_dump(),
        }
        paginate_data_validated = self.validate(
            paginate_data_dict,
            actions_repositories_models.PaginateRequestBaseModel,
        )

        response = await self.collection.get_batch(paginate_data_validated)

        response_validated = self.validate(
            response.model_dump(by_alias=True),
            actions_services_models.ReviewListPaginateModel,
        )
        return response_validated


@functools.lru_cache()
def get_review_service(
    database: motor_core.AgnosticDatabase = fastapi.Depends(clients.get_mongo_db),
):
    return ReviewService(database)

# pyright: reportIncompatibleMethodOverride=false


import functools

import fastapi
import libs.actions.repositories.models as actions_repositories_models
import libs.actions.services.base as actions_services_base
import libs.actions.services.models as actions_services_models
import libs.actions.utils as actions_utils
import libs.clients as clients
import motor.core as motor_core


class LikeService(actions_services_base.BaseService):
    @property
    def name(self) -> str:
        return "like"

    async def create_one(
        self,
        create_data: actions_services_models.LikeCreateModel,
    ) -> actions_services_models.LikeFullResponseModel:
        create_data_dict = create_data.model_dump()
        create_data_validated = self.validate(
            create_data_dict, actions_repositories_models.CreateRequestBaseModel
        )
        search_data_validated = self.validate(
            {
                "user_id": create_data_dict["user_id"],
                "item_id": create_data_dict["item_id"],
            },
            actions_repositories_models.SearchRequestBaseModel,
        )
        response = await self.collection.create_or_update_one(
            search_data=search_data_validated,
            create_data=create_data_validated,
        )

        response_validated = self.validate(
            response.model_dump(by_alias=True),
            actions_services_models.LikeFullResponseModel,
        )
        return response_validated

    async def get_one(
        self,
        search_data: actions_services_models.LikeSearchModel,
    ) -> actions_services_models.LikeFullResponseModel | None:
        search_data_validated = self.validate(
            search_data.model_dump(exclude_none=True, by_alias=True),
            actions_repositories_models.SearchRequestBaseModel,
        )

        response = await self.collection.get_one(search_data_validated)
        if response is None:
            return response

        response_validated = self.validate(
            response.model_dump(by_alias=True),
            actions_services_models.LikeFullResponseModel,
        )
        return response_validated

    async def delete_one(
        self,
        search_data: actions_services_models.LikeSearchModel,
    ) -> actions_services_models.LikeFullResponseModel | None:
        search_data_validated = self.validate(
            search_data.model_dump(exclude_none=True, by_alias=True),
            actions_repositories_models.SearchRequestBaseModel,
        )
        response = await self.collection.get_and_delete_one(search_data_validated)
        if response is None:
            return response

        response_validated = self.validate(
            response.model_dump(by_alias=True),
            actions_services_models.LikeFullResponseModel,
        )
        return response_validated

    async def get_item_rating(
        self,
        rating_data: actions_services_models.LikeRatingRequest,
    ) -> int | float | None:
        search_data = actions_services_models.LikeSearchModel(
            item_id=rating_data.item_id, item_type=rating_data.item_type
        )
        search_data_dict = {
            "field_names": ["rating"],
            **search_data.model_dump(exclude_none=True),
        }
        search_data_validated = self.validate(
            search_data_dict,
            actions_repositories_models.SearchRequestBaseModel,
        )

        response = await self.collection.get_all(search_data_validated)
        response_validated = self.validate(
            response.model_dump(), actions_services_models.LikeRatingListResponse
        )
        if rating_data.item_type == actions_utils.ItemTypeEnum.MOVIE:
            return response_validated.get_average_rating()
        return response_validated.get_rating_likes_count()


@functools.lru_cache()
def get_like_service(
    client: motor_core.AgnosticDatabase = fastapi.Depends(clients.get_mongo_db),
):
    return LikeService(client)

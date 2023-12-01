import logging

import backoff
import fastapi
import libs.actions.handlers as actions_handlers
import libs.app.config as config
import libs.clients.mongo as clients_mongo
import motor.motor_asyncio as motor_asyncio
import pymongo.errors as pymongo_errors

logger = logging.getLogger(__name__)


class Application:
    def __init__(self) -> None:
        self.settings = config.base_settings
        self.mongo_settings = config.mongo_settings

    def create_app(self) -> fastapi.FastAPI:
        app = fastapi.FastAPI(
            title=self.settings.project_name,
            description=self.settings.project_description,
            version=self.settings.project_version,
            docs_url="/api/openapi",
            openapi_url="/api/openapi.json",
            default_response_class=fastapi.responses.ORJSONResponse,
        )

        app.include_router(
            actions_handlers.likes_router,
            prefix="/api/v1/actions/likes",
            tags=["likes"],
        )
        app.include_router(
            actions_handlers.review_router,
            prefix="/api/v1/actions/reviews",
            tags=["reviews"],
        )
        app.include_router(
            actions_handlers.bookmark_router,
            prefix="/api/v1/actions/bookmarks",
            tags=["bookmarks"],
        )

        @app.on_event("startup")
        @backoff.on_exception(
            backoff.expo,
            pymongo_errors.ServerSelectionTimeoutError,
            base=2,
            factor=1,
            max_value=60,
            max_tries=None,
        )
        async def startup_event():  # type: ignore[reportUnusedFunction]
            logger.info("Starting server")

            client = motor_asyncio.AsyncIOMotorClient(  # type: ignore[reportUnknownVariableType]
                self.mongo_settings.get_url()
            )
            logger.info(f"{await client.server_info()}")
            clients_mongo.mongo_database = client[self.mongo_settings.mongo_db_name]

        @app.on_event("shutdown")
        async def shutdown_event():  # type: ignore[reportUnusedFunction]
            logger.info("Shutting down server")

        return app

import pydantic
import pydantic_settings


class MongoSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    mongo_db_name: str = pydantic.Field(default="action", alias="MONGO_DB_NAME")
    mongo_user: str = pydantic.Field(default=..., alias="MONGO_USER")
    mongo_pass: str = pydantic.Field(default=..., alias="MONGO_PASS")
    mongo_host: str = pydantic.Field(default="localhost", alias="MONGO_HOST")
    mongo_port: str = pydantic.Field(default="27019", alias="MONGO_PORT")

    def get_url(self):
        return (
            f"mongodb://{self.mongo_user}:{self.mongo_pass}@"
            f"{self.mongo_host}:{self.mongo_port}/?authMechanism=DEFAULT"
        )

import pydantic
import pydantic_settings


class BaseSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    project_name: str = pydantic.Field(default="Action API", alias="PROJECT_NAME")
    project_description: str = pydantic.Field(
        default="Action API DDD", alias="PROJECT_DESCRIPTION"
    )
    project_version: str = pydantic.Field(default="1.0.0", alias="PROJECT_VERSION")

    server_host: str = pydantic.Field(default="0.0.0.0", alias="ACTION_HOST")
    server_port: int = pydantic.Field(default=8000, alias="ACTION_PORT")

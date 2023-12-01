import pydantic
import pydantic_settings


class TestsSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    api_protocol: str = pydantic.Field(default="http", alias="ACTION_PROTOCOL")
    api_host: str = pydantic.Field(default="0.0.0.0", alias="ACTION_HOST")
    api_port: str = pydantic.Field(default="8000", alias="ACTION_PORT")

    jwt_secret_key: str = pydantic.Field(default=..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = pydantic.Field(default="HS256", alias="TOKEN_SIGN_ALGORITHM")

    def get_api_url(self):
        return f"{self.api_protocol}://{self.api_host}:{self.api_port}/api/v1/actions/"


tests_settings = TestsSettings()
